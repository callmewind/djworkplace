from django.conf import settings
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import *

class Holiday(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), related_name='holidays')
    start = models.DateField(_('start'))
    end = models.DateField(_('end'))
    approval_date = models.DateTimeField(blank=True, null=True, editable=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('approved by'), related_name='holiday_approvals', blank=True, null=True)

    def calendar_text(self):
    	return str(self.user)

    def __str__(self):
        return "%d %s - %s" % (self.user_id, self.start, self.end)

    def clean(self):
        super().clean()
        if not self.user.staffprofile.department:
            raise ValidationError('%s must be in a department first' % self.user)
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


@receiver(post_save, sender=Holiday)
def createStaffProfile(sender, instance, created, **kwargs):
    if created and not instance.approval_date:
        transaction.on_commit(lambda: sendHolidayRequestEmail.delay(args=(instance.pk,)))

