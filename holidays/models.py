from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

class Holiday(models.Model):
    calendar_template = 'holidays/event.html'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), related_name='holidays')
    start = models.DateField(_('start'))
    end = models.DateField(_('end'))
    approval_date = models.DateTimeField(blank=True, null=True, editable=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('approved by'), related_name='holiday_approvals', blank=True, null=True)

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
        collisions = Holiday.objects.filter(user=self.user).exclude(pk=self.pk).filter(
            start_collision|end_collision|contained_collission
        )
        if collisions.exists():
            raise ValidationError('There are other holidays requests with some colliding days')

        if self.approved_by:
            if not self.user.staffprofile.department.managers.filter(pk=self.approved_by.pk).exists():
                raise ValidationError('%s is not a manager of %s department' % (self.approved_by, self.user.staffprofile.department))
            if not self.approval_date:
                self.approval_date = timezone.now()
        else:
            self.approval_date = None

    class Meta:
        ordering = ['-start', '-end']
        verbose_name = _('holidays')
        verbose_name_plural = _('holidays')


