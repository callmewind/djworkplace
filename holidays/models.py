from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Holidays(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user') )
	start = models.DateField(_('start'))
	end = models.DateField(_('end'))
