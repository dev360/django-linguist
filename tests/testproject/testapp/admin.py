from django.contrib import admin

from testapp.models import Product, ProductTranslation


class ProductTranslationInline(admin.TabularInline):
    model = ProductTranslation

class ProductAdmin(admin.ModelAdmin):
    model = Product
admin.site.register(Product, ProductAdmin)
