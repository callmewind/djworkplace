from django import forms
from .models import *

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['start', 'end',]
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
        }