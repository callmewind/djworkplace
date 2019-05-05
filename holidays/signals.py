from holidays.models import *
from datetime import timedelta
from django.db import transaction
from django.db.models.signals import post_save
from staff.signals import calendar_display
from staff.views import CalendarView
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

@receiver(post_save, sender=Holiday)
def onHolidayRequest(sender, instance, created, **kwargs):
    if created and not instance.approval_date:
        from djworkplace.tasks import enqueue_mail
        transaction.on_commit(lambda: enqueue_mail(
                _('Holiday request'),
                _("%s is requesting a holiday period from %s to %s") % (instance.user, instance.start, instance.end),
                [manager.email for manager in instance.user.staffprofile.department.managers.all()]
            )
        )

@receiver(calendar_display, sender=CalendarView)
def on_calendar_display(sender, days, department, location, **kwargs):
    day_list = list(days.keys())
    first_day_of_calendar = next(iter(day_list))
    last_day_of_calendar = next(reversed(day_list)) 

    holidays = Holiday.objects.filter(Q(start__range=(first_day_of_calendar, last_day_of_calendar))|Q(end__range=(first_day_of_calendar, last_day_of_calendar)))
    if department:
        holidays = holidays.filter(user__staffprofile__department=department)
    if location:
        holidays = holidays.filter(user__staffprofile__location=location)

    for holiday in holidays:
        day = max(holiday.start, first_day_of_calendar)
        while day <= min(holiday.end, last_day_of_calendar):
            days[day]['events'].append(holiday)
            day = day + timedelta(days=1)

