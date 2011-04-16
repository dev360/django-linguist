from django.db import models
from django.utils.translation import ugettext_lazy as _


from linguist.models import TranslationModel

class Product(models.Model):
    model_number = models.CharField(_('model number'), max_length=16)
    
    def __unicode__(self):
        return "%s" % self.model_number
    

class ProductTranslation(TranslationModel):
    model_to_translate = Product
    
    def __unicode__(self):
        return "%s" % self.pk
    
    title = models.CharField(_('title'), max_length=128)
    description = models.CharField(_('description'), max_length=128)
    price = models.DecimalField(_('price'), decimal_places=2,max_digits=6)
    visible = models.BooleanField(_('visible'), default=False)
    
    