from django import forms
from .models import *

class VacationsForm(forms.ModelForm):

    def clean_user(self):
        return self.initial['user']

    class Meta:
        model = Vacation
        fields = ['start', 'end', 'user']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
            'user': forms.HiddenInput
        }