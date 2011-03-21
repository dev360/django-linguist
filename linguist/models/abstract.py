from django.db import models
from django.db.models.base import ModelBase

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
                model.add_to_class('parent', models.ForeignKey(model.model_to_translate))
                
                # Add uniqueness constraints
                model.Meta.unique_together = ['parent', 'locale']
        
        return model

        
class TranslationModel(models.Model):
    __metaclass__ = TranslationModelBase
    locale = models.CharField(max_length=5)
    
    class Meta:
        abstract = True

