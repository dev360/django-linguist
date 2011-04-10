from django.conf import settings
from django import template

register = template.Library()

def sort_language(a, b):
    str_a = getattr(a.form, "language_name", "")
    str_b = getattr(b.form, "language_name", "")
    return cmp(str_a, str_b)
    

@register.filter
def order_by_language(forms):
    return sorted(list(forms), cmp=sort_language)
    