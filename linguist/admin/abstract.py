from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.contrib.admin.options import InlineModelAdmin
from django.db import transaction
from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.forms.util import ErrorList

from types import TupleType

try:
    type(set)
except:
    from sets import Set as set

csrf_protect_m = method_decorator(csrf_protect)

class TranslationAdmin(ModelAdmin):
    
    def __init__(self, *args, **kwargs):
        super(TranslationAdmin, self).__init__(*args, **kwargs)
    

class TranslationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TranslationForm, self).__init__(*args, **kwargs)
        self.fields['locale'].widget = forms.HiddenInput()
    
    
    def _get_required_languages(self):
        if hasattr(settings, 'TRANSLATION_REQUIRED_LANGUAGES') and len(settings.TRANSLATION_REQUIRED_LANGUAGES) > 0:
            if type(settings.TRANSLATION_REQUIRED_LANGUAGES[0]) is TupleType:
                return (x[0] for x in settings.TRANSLATION_REQUIRED_LANGUAGES)
            else:
                return settings.TRANSLATION_REQUIRED_LANGUAGES
        else:
            return []
    
    def _get_changed_data(self):
        changed_data = super(TranslationForm, self)._get_changed_data()
        if len(changed_data) == 1 and changed_data[0] == 'locale':
            
            locale_field = self.add_prefix('locale')
            locale = self.data[locale_field]
            required_languages = self._get_required_languages()
            
            if locale not in required_languages:
                changed_data.remove('locale')
            
        return changed_data
    changed_data = property(_get_changed_data)
    
    
def _get_friendly_name(locale):
    matches = [x[1] for x in settings.LANGUAGES if x[0] == locale]
    if matches and len(matches) == 1:
        return matches[0]
    return None

class TranslationFormSet(BaseInlineFormSet):
    
    extra_languages = None
    
    def __init__(self, *args, **kwargs):
        super(TranslationFormSet, self).__init__(*args, **kwargs)
    
    
    def _set_languages(self):
        if self.extra_languages == None:
            
            initial_forms = super(TranslationFormSet, self)._get_initial_forms()
            
            self.all_languages = set([lang[0] for lang in settings.LANGUAGES])
            self.initial_languages = set([form.initial['locale'] for form in initial_forms])
            self.extra_languages = self.all_languages - self.initial_languages
    
    
    def _get_initial_forms(self):
        self._set_languages()
        initial_forms = super(TranslationFormSet, self)._get_initial_forms()
        
        # Hack-Hack!
        for form in initial_forms:
            form.language = form.initial['locale']
            form.language_name = _get_friendly_name(form.language)
            form.required_languages = [('en-us', 'English')]
        return initial_forms
    initial_forms = property(_get_initial_forms)
    
    
    def _get_extra_forms(self):
        self._set_languages()
        forms = self.forms[len(self.initial_languages):]
        
        for form, language in zip(forms, self.extra_languages):
            form.initial['locale'] = language
            form.language = language
            form.language_name = _get_friendly_name(form.language)
        return forms
    
    extra_forms = property(_get_extra_forms)
    
    
    def sort_by_locale(a, b):
        return a.initial['locale'] == b.initial['locale']
    
    
    
class TranslationInline(InlineModelAdmin):
    
    
    def queryset(self, request):
        qs = super(TranslationInline, self).queryset(request)
        return qs
    
    
    def __init__(self, *args, **kwargs):
        super(TranslationInline, self).__init__(*args, **kwargs)
    
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(TranslationInline, self).get_formset(request, obj=None, **kwargs)
        return formset
    
    
    extra = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)
    form = TranslationForm
    formset = TranslationFormSet
    template = 'admin/translation_inline.html'
    