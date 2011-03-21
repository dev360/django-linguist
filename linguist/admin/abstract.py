from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.contrib.admin.options import InlineModelAdmin
from django.db import transaction
from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.forms.util import ErrorList

from sets import Set

csrf_protect_m = method_decorator(csrf_protect)

class TranslationAdmin(ModelAdmin):
    
    def __init__(self, *args, **kwargs):
        super(TranslationAdmin, self).__init__(*args, **kwargs)
    

class TranslationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TranslationForm, self).__init__(*args, **kwargs)
        self.fields['locale'].widget = forms.HiddenInput()
    
    

class TranslationFormSet(BaseInlineFormSet):
    
    extra_languages = None
    
    def _get_initial_forms(self):
        uber = super(TranslationFormSet, self)._get_initial_forms()
        
        if self.extra_languages == None:
            # Set the extra_languages property.
            self.all_languages = Set([lang[0] for lang in settings.LANGUAGES])
            self.initial_languages = Set([form.initial['locale'] for form in uber])
            self.extra_languages = self.all_languages - self.initial_languages
        
        return uber
    initial_forms = property(_get_initial_forms)
    
    def _get_extra_forms(self):
        forms = self.forms[len(self.initial_languages):]
        
        for form, language in zip(forms, self.extra_languages):
            form.initial['locale'] = language
        return forms
        
    extra_forms = property(_get_extra_forms)
    
    def __init__(self, *args, **kwargs):
        super(TranslationFormSet, self).__init__(*args, **kwargs)
    

class TranslationInline(InlineModelAdmin):
    
    def queryset(self, request):
        qs = super(TranslationInline, self).queryset(request)
        return qs
    
    def _construct_forms(self):
        super(TranslationInline, self)._construct_forms()
    
    
    def __init__(self, *args, **kwargs):
        super(TranslationInline, self).__init__(*args, **kwargs)
    
    #tabbed_inline_admin_form
    
    extra = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)
    form = TranslationForm
    formset = TranslationFormSet
    template = 'admin/translation_inline.html'