from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from staff.models import *

calendar_display = Signal(providing_args=["days", "department", "location"])

@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="staff.onUserCreation")
def on_user_creation(sender, instance, created, **kwargs):
    if created:
        StaffProfile.objects.create(user=instance)
