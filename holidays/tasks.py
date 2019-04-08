from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from holidays.models import *

@shared_task
def sendHolidayRequestEmail(holiday_pk):
    try:
        holiday = Holiday.objects.get(pk=holiday_pk)
        send_mail(
            _('Holiday request'),
            'Here is the message.',
            'from@example.com',
            [manager.email for manager in holiday.user.staffprofile.department.managers.all()]
        )
    except Holiday.DoesNotExist:
        pass

