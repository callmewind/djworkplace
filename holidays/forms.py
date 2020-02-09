from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import *
from datetime import date

class LeaveForm(forms.ModelForm):

    year = forms.TypedChoiceField(label=_('year'), coerce=int)

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = user
        self.fields['type'].queryset = self.fields['type'].queryset.filter(department_leaves__department=user.staffprofile.department)
        year = date.today().year
        max_date = datetime.date(year, 4, 1) - datetime.timedelta(days=1)
        if max_date > date.today():
            self.fields['year'].choices = ((year - 1, year - 1), (year, year),)
        else:
            self.fields['year'].choices = ((year, year),)



    class Meta:
        model = Leave
        fields = ['type', 'start', 'end', 'notes', 'year']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
        }


class AdminLeaveForm(forms.ModelForm):

    approve = forms.BooleanField(label=_('Approve request'), required=False, help_text=_('check if you want to approve this request'))

    class Meta:
        model = Leave
        fields = ['type', 'start', 'end', 'notes']