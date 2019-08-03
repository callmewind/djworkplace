from django import forms
from .models import *

class LeaveForm(forms.ModelForm):

    def clean_user(self):
        return self.initial['user']

    class Meta:
        model = Leave
        fields = ['start', 'end', 'user', 'notes']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
            'user': forms.HiddenInput
        }