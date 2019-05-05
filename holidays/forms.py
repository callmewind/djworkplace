from django import forms
from .models import *

class HolidayForm(forms.ModelForm):

    def clean_user(self):
        return self.initial['user']

    class Meta:
        model = Holiday
        fields = ['start', 'end', 'user']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
            'user': forms.HiddenInput
        }