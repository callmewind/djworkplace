from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Holiday(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), related_name='holidays')
    start = models.DateField(_('start'))
    end = models.DateField(_('end'))


    def __str__(self):
        return "%d %s - %s" % (self.user_id, self.start, self.end)

    class Meta:
        ordering = ['-start', '-end']
        verbose_name = _('holidays')
        verbose_name_plural = _('holidays')
