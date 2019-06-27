from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver, Signal
from django.urls import reverse
from staff.models import *

calendar_display = Signal(providing_args=["days", "department", "location"])

@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="staff.onUserCreation")
def on_user_creation(sender, instance, created, **kwargs):
    if created:
        StaffProfile.objects.create(user=instance)
        from djworkplace.tasks import enqueue_mail
        transaction.on_commit(lambda: enqueue_mail(
                _('Welcome to %s') % settings.APP_NAME,
                _("If your manager didn't give your password, you can generate one here: %s") % reverse('password_reset'),
                [instance.email]
            )
        )