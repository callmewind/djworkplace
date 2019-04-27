from holidays.models import *
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

@receiver(post_save, sender=Holiday, dispatch_uid="holidays.onHolidayRequest")
def onHolidayRequest(sender, instance, created, **kwargs):
    if created and not instance.approval_date:
        from djworkplace.tasks import enqueue_mail
        transaction.on_commit(lambda: enqueue_mail(
                _('Holiday request'),
                _("%s is requesting a holiday period from %s to %s") % (instance.user, instance.start, instance.end),
                [manager.email for manager in instance.user.staffprofile.department.managers.all()]
            )
        )