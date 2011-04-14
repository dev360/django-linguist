===============
Django Linguist
===============

Django Linguist is a light-weight approach to localizing your models.

How it works
------------
Your translations are stored in a separate model and you can use the admin
to edit your translation via tabs.

Requirements
------------
- Django 1.3
- Python 2.6


How to use it
-------------

Add 'linguist' to your installed apps, then modify your admin.py and models.py as follows:


** models.py **
from django.db import models
from django.utils.translation import ugettext_lazy as _


from linguist.models import TranslationModel

class Product(models.Model):
    model_number = models.CharField(_('model number'), max_length=16)


class ProductTranslation(TranslationModel):
    model_to_translate = Product
    
    title = models.CharField(_('title'), max_length=128)
    description = models.CharField(_('description'), max_length=128)
    price = models.DecimalField(_('price'), decimal_places=2,max_digits=6)
    visible = models.BooleanField(_('visible'), default=False)


** admin.py **
from django.contrib import admin
from django.conf import settings

from linguist.admin import TranslationInline, TranslationAdmin

from testapp.models import Product, ProductTranslation


class ProductTranslationInline(TranslationInline):
    model = ProductTranslation

class ProductAdmin(TranslationAdmin):
    inlines = [ProductTranslationInline,]
    model = Product
admin.site.register(Product, ProductAdmin)


