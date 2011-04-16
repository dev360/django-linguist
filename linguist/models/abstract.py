from django.db import models
from django.db.models.base import ModelBase
from django.conf import settings


class TranslationModelBase(ModelBase):
    
    def __new__(cls, name, bases, attrs):
        model = super(TranslationModelBase, cls).__new__(cls, name, bases, attrs)
        
        for b in bases:
            if b.__name__=="TranslationModel":
                if not hasattr(model, 'model_to_translate'):
                    raise Exception('%s must define the model_to_translate property if deriving from the TranslationModel class.' % (name,))
                elif type(model.model_to_translate.__class__) != type(type):
                    raise Exception('%s.model_to_translate must be a type declaration.' % (name,))
                
                # Now set the dynamic field
                model.add_to_class('parent', models.ForeignKey(model.model_to_translate, related_name='translations'))
                
                # Add uniqueness constraints
                model._meta.unique_together = (('parent', 'locale'),)
        
        return model


class TranslationQuerySet(models.query.QuerySet):
    
    def _correct_fieldname(self, field_query, fields):
        field_arr = field_query.split('__')
        # 
        # Two variations here; either the field name was passed in
        # by itself without arguments, or had something on the end;
        # i.e. bar=foo OR bar__exact=foo or similar. We need to get 
        # `bar` out of that string either way.
        #
        field_name = field_arr[0] if len(field_arr) > 0 else field_query 
        
        if field_name not in ('pk','id') and field_name not in fields:
            return 'parent__'+field_query
        else:
            return field_query
    
    
    def order_by(self, *field_names):
        # Order by needs to be corrected too.
        fields = self.model._meta.get_all_field_names()
        new_field_names = []
        for field_name in field_names:
            new_field_names.append(self._correct_fieldname(field_name, fields))
        return super(TranslationQuerySet, self).order_by(*new_field_names)
    
    
    def _filter_or_exclude(self, negate, *args, **kwargs):
        """ 
        We have to override the query to prepend `parent__` to
        query arguments which do not seem to contain an attribute
        that is part of the model.. this way we can construct
        queries using attributes that belong to the parent.
        """
        
        fields = self.model._meta.get_all_field_names()
        
        new_args = []
        for arg in args:
            if type(arg) is models.query_utils.Q:
                new_children = []
                for child in arg.children:
                    if len(child) == 2:
                        corrected_query = self._correct_fieldname(child[0], fields)
                        new_children.append((corrected_query, child[1]))
                    else:
                        new_children.append(child) # Just to be on the safe side.                
                arg.children = new_children
                new_args.append(arg)
            else:
                new_args.append(arg)
        
        new_kwargs = {}
        for field_query in kwargs.keys():
            corrected_query = self._correct_fieldname(field_query, fields)
            new_kwargs[corrected_query] = kwargs[field_query]

        return super(TranslationQuerySet, self)._filter_or_exclude(negate, *new_args, **new_kwargs)


class TranslationModelManager(models.Manager):
    
    def get_query_set(self):    
        qs = TranslationQuerySet(self.model)
        return qs.select_related('parent')

        
class TranslationModel(models.Model):
    __metaclass__ = TranslationModelBase
    
    locale = models.CharField(max_length=5, db_index=True, choices=settings.LANGUAGES)
    
    objects = TranslationModelManager()
    
    
    def __getattribute__(self, attr):
        """ Override __getattribute__ so that we can get the parent properties. We don't care about setters. """
        try:
            return super(TranslationModel, self).__getattribute__(attr)
        except:
            if attr != 'pk' and attr in self.model_to_translate._meta.get_all_field_names():
                parent = super(TranslationModel, self).__getattribute__('parent')
                return super(models.Model, parent).__getattribute__(attr)
            else:
                raise
    
    class Meta:
        abstract = True

