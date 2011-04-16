===============
Django Linguist
===============

Django Linguist is a light-weight approach to localizing your models.

How it works
------------
Your translations are stored in a separate model and you can use the admin
to edit your translation via tabs.

In general terms, the structure is as follows:

	Foo 1 --- * FooTranslation

In this case, all translations for Foo must reside in the FooTranslation class,
which contains a property `locale` which is unique_together with the reference
back to Foo's id to avoid duplicate translations for an instance of Foo. The
locales are read from the LANGUAGES setting.

In this scenario, given, the instances foo and foo_translation will follow the
conventions below:

 - foo_translation.parent  
   returns the parent class, Foo.
 - foo.translations
   returns all the translations for the instance foo.


Capabilities
------------
- Renders in admin with tabs for each language when you use the TranslationInline
  and TranslationAdmin.
- You can specify a global setting, TRANSLATION_REQUIRED_LANGUAGES to enumerate
  the languages that you want to be required in admin, if any.
- Allows convenient access to the parent with the `parent` attribute.
- Allows convenient access to the translations with the `translations` attribute.
- The manager for the translations will ensure that parents are retrieved together
  with the translations (i.e. it uses select_related).


Missing capabilities
--------------------
- There is currently no locale middleware implemented, so all lookups require you
  to pass in filter(locale=XXX) to retrieve your translations.
- There is a little dilemma in how to treat many to many, or one to many relationships
  between the parent class and other related classes, e.g. Product 1 - * Product Feature
  etc. It would be ideal if there was a convenient way to edit these in the admin
  and if it could be achieved without any mind-bending db schemas.
- The form for a translated object can not account for any property in the parent.
  The only thing this code does is forward attribute lookups on the translated object
  back to the parent, but setting attribute on the parent object via the translated object
  is not supported.


Requirements
------------
I have only tested with the following:

- Django 1.3
- Python 2.6/2.7


How to use it
-------------

Add 'linguist' to your installed apps, then modify your admin.py and models.py as follows:


*** models.py ***  
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


*** admin.py ***  
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


