from holidays.models import *
from holidays.tasks import *
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Holiday, dispatch_uid="holidays.onHolidayRequest")
def onHolidayRequest(sender, instance, created, **kwargs):
    if created and not instance.approval_date:
        transaction.on_commit(lambda: sendHolidayRequestEmail.delay(instance.pk,))