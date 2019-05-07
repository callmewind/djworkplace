from django.conf import settings
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Department(models.Model):
    name = models.CharField(_('name'), max_length=200)
    vacations = models.PositiveSmallIntegerField(_('vacations'), help_text=_('Yearly vacation days'))
    personal_days = models.PositiveSmallIntegerField(_('personal days'), help_text=_('Yearly personal days'))
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('managers'), related_name='managed_departments')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('department')
        verbose_name_plural = _('departments')

class Location(models.Model):
    name = models.CharField(_('name'), max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('location')
        verbose_name_plural = _('locations')


class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), editable=False)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name=_('department'), blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name=_('location'), blank=True, null=True)
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = _('staff profile')
        verbose_name_plural = _('staff profiles')
