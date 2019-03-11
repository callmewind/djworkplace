from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Department(models.Model):
    name = models.CharField(_('name'), max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = _('department')
        verbose_name_plural = _('departments')


class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user') )
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name=_('department'))

    class Meta:
        verbose_name = _('staff profile')
        verbose_name_plural = _('staff profiles')


