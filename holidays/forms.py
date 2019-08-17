from django import forms
from .models import *

class LeaveForm(forms.ModelForm):

    user = None

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = user
        self.fields['type'].queryset = self.fields['type'].queryset.filter(department_leaves__department=user.staffprofile.department)

    class Meta:
        model = Leave
        fields = ['type', 'start', 'end', 'notes']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
        }