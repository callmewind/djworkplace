from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import *

class LeaveForm(forms.ModelForm):

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


class AdminLeaveForm(forms.ModelForm):

    approve = forms.BooleanField(label=_('Approve request'), required=False, help_text=_('check if you want to approve this request'))

    class Meta:
        model = Leave
        fields = ['type', 'start', 'end', 'notes']