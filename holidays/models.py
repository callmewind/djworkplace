from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from staff.models import Location

class Vacation(models.Model):
    calendar_template = 'holidays/vacations_event.html'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), related_name='vacations')
    start = models.DateField(_('start'))
    end = models.DateField(_('end'))
    approval_date = models.DateTimeField(blank=True, null=True, editable=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('approved by'), related_name='vacation_approvals', blank=True, null=True)

    def __str__(self):
        return "%d %s - %s" % (self.user_id, self.start, self.end)

    def clean(self):
        super().clean()
        if not self.user.staffprofile.department:
            raise ValidationError('%s must be in a department first' % self.user)

        if self.end < self.start:
            raise ValidationError("End date can't be before start date")

        start_collision = Q(start__lte=self.start, end__gte=self.start)
        end_collision = Q(start__lte=self.end, end__gte=self.end)
        contained_collission = Q(start__gte=self.start, end__lte=self.end)
        collisions = Vacation.objects.filter(user=self.user).exclude(pk=self.pk).filter(
            start_collision|end_collision|contained_collission
        )
        if collisions.exists():
            raise ValidationError('There are other vacations requests with some colliding days')

        if self.approved_by:
            if not self.user.staffprofile.department.managers.filter(pk=self.approved_by.pk).exists():
                raise ValidationError('%s is not a manager of %s department' % (self.approved_by, self.user.staffprofile.department))
            if not self.approval_date:
                self.approval_date = timezone.now()
        else:
            self.approval_date = None

    class Meta:
        ordering = ['-start', '-end']
        verbose_name = _('vacations')
        verbose_name_plural = _('vacations')

class PublicHoliday(models.Model):
    calendar_template = 'holidays/holiday_event.html'
    date = models.DateField(_('date'))
    yearly = models.BooleanField(_('yearly'))
    name = models.CharField(_('name'), max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name=_('location'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['yearly', '-date']
        verbose_name = _('public holiday')
        verbose_name_plural = _('public holidays')
