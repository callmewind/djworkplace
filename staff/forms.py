from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _

class CalendarFilterForm(forms.Form):
	department = forms.ModelChoiceField(label=_('department'), queryset=Department.objects.all(), required=False, empty_label=_('Filter department'))
	location = forms.ModelChoiceField(label=_('location'), queryset=Location.objects.all(), required=False, empty_label=_('Filter location'))
