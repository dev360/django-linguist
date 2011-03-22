from django.contrib import admin

from linguist.admin import TranslationInline, TranslationAdmin

from testapp.models import Product, ProductTranslation


class ProductTranslationInline(TranslationInline):
    model = ProductTranslation

class ProductAdmin(TranslationAdmin):
    inlines = [ProductTranslationInline,]
    model = Product
admin.site.register(Product, ProductAdmin)
