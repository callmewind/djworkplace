from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from staff.models import Location, Department
from django.contrib.auth import get_user_model
from .managers import *
from .utils import location_holiday_dates, is_working_day

class LeaveType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=3)

    def __str__(self):
        return "%s %s" % (self.icon, self.name,)

    class Meta:
        ordering = ['name']
        verbose_name = _('leave type')
        verbose_name_plural = _('leave types')

class LeaveLimit(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name=_('department'), related_name='leave_limits')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name=_('location'), related_name='leave_limits')
    type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, verbose_name=_('type'), related_name='department_leaves')
    days = models.PositiveSmallIntegerField(verbose_name=_('days'), help_text=_('Yearly permission days for this type'))

    class Meta:
        ordering = ['department', 'location']
        verbose_name = _('leave limit')
        verbose_name_plural = _('leave limits')
        unique_together = (('department', 'location', 'type'),)

    def __str__(self):
        return "%d/%d/%d - %d" % (self.department_id, self.location_id, self.type_id, self.days)

class Leave(models.Model):
    calendar_template = 'holidays/leave_event.html'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), related_name='leaves', editable=False)
    type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, verbose_name=_('type'), related_name='leaves')
    start = models.DateField(_('start'))
    end = models.DateField(_('end'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    approval_date = models.DateTimeField(blank=True, null=True, editable=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('approved by'), related_name='vacation_approvals', blank=True, null=True, editable=False)
    notes = models.TextField(blank=True, max_length=500)
    year = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return "%d %s - %s" % (self.user_id, self.start, self.end)

    def dates(self):
        return (self.start + timedelta(days=d) for d in range((self.end - self.start).days + 1))

    def working_dates(self):
        return (d for d in self.dates() if is_working_day(d, self.user.staffprofile.location))

    def working_days(self):
        return len(list(self.working_dates()))

    def clean(self):
        super().clean()
        if not self.user.staffprofile.department:
            raise ValidationError('%s must be in a department first' % self.user)

        if self.end < self.start:
            raise ValidationError("End date can't be before start date")

        start_collision = Q(start__lte=self.start, end__gte=self.start)
        end_collision = Q(start__lte=self.end, end__gte=self.end)
        contained_collission = Q(start__gte=self.start, end__lte=self.end)
        collisions = Leave.objects.filter(user=self.user).exclude(pk=self.pk).filter(
            start_collision|end_collision|contained_collission
        )
        if collisions.exists():
            raise ValidationError('There are other leave requests with one or more days colliding')

        if self.approved_by:
            if not self.user.staffprofile.department.managers.filter(pk=self.approved_by.pk).exists():
                raise ValidationError('%s is not a manager of %s department' % (self.approved_by, self.user.staffprofile.department))

    def save(self, *args, **kwargs):
        if self.approved_by:
            if not self.approval_date:
                self.approval_date = timezone.now()
        else:
            self.approval_date = None
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start', '-end']
        verbose_name = _('leave')
        verbose_name_plural = _('leaves')

class PublicHoliday(models.Model):
    objects = PublicHolidayManager()
    calendar_template = 'holidays/holiday_event.html'
    date = models.DateField(_('date'))
    yearly = models.BooleanField(_('yearly'))
    name = models.CharField(_('name'), max_length=200)
    locations = models.ManyToManyField(Location, verbose_name=_('locations'), related_name='local_holidays')

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['yearly', '-date']
        verbose_name = _('public holiday')
        verbose_name_plural = _('public holidays')

class UserLeave(get_user_model()):

    def current_year_approved_leaves(self, type):
        year = timezone.now().year
        count = 0  
        for v in Leave.objects.filter(user=self, type=type).filter(Q(start__year=year)|Q(end__year=year), approval_date__isnull=False):
            count += len([d for d in v.working_dates() if d.year == year])
        return count

    def current_year_pending_leaves(self, type):
        from holidays.models import Leave
        year = timezone.now().year
        count = 0  
        for v in Leave.objects.filter(user=self, type=type).filter(Q(start__year=year)|Q(end__year=year), approval_date__isnull=True):
            count += len([d for d in v.working_dates() if d.year == year])
        return count
    
    class Meta:
        proxy = True
        verbose_name = _('user leaves')
        verbose_name_plural = _('users leaves')
