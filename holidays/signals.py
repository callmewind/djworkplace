from holidays.models import *
from datetime import timedelta
from django.db import transaction
from django.db.models.signals import post_save
from staff.signals import calendar_display
from staff.views import CalendarView
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from .utils import is_working_day

@receiver(post_save, sender=Leave)
def on_leave_request(sender, instance, created, **kwargs):
    if created and not instance.approval_date:
        from djworkplace.tasks import enqueue_mail
        transaction.on_commit(lambda: enqueue_mail(
                [ manager.email for manager in instance.user.staffprofile.department.managers.all() ],
                _('%s request') % instance.type,
                template='holidays/email/leave_request.html',
                context={ 'leave' : instance }
            )
        )

@receiver(post_save, sender=Leave)
def on_leave_approval(sender, instance, created, **kwargs):
    if instance.approval_date and not (instance.updated - instance.approval_date).seconds:
        from djworkplace.tasks import enqueue_mail
        transaction.on_commit(lambda: enqueue_mail(
                [ instance.user.email ],
                _('Leave request approved'),
                _("Your %s request from %s to %s has been approved") % (instance.type, instance.start, instance.end),
            )
        )

@receiver(calendar_display, sender=CalendarView)
def on_calendar_display(sender, days, months, department, location, **kwargs):

    day_list = list(days.keys())
    first_day_of_calendar = next(iter(day_list))
    last_day_of_calendar = next(reversed(day_list)) 

    public_holidays = PublicHoliday.objects.filter(
        Q(date__gte=first_day_of_calendar, date__lte=last_day_of_calendar)|
        Q(date__month__in=months, yearly=True)
    )

    if location:
        public_holidays = public_holidays.filter(Q(location__isnull=True)|Q(location=location))

    public_holidays_dates = list()

    for holiday in public_holidays:
        if holiday.date in days:
            days[holiday.date]['events'].append(holiday)
            public_holidays_dates.append(holiday.date)
        elif holiday.yearly: #try to fit yearly events
            for y in range(first_day_of_calendar.year, last_day_of_calendar.year + 1):
                holiday.date = holiday.date.replace(year=y)
                if holiday.date in days:
                    days[holiday.date]['events'].append(holiday)
                    public_holidays_dates.append(holiday.date)
                    break

    

    leaves = Leave.objects.filter(Q(start__range=(first_day_of_calendar, last_day_of_calendar))|Q(end__range=(first_day_of_calendar, last_day_of_calendar)))
    if department:
        leaves = leaves.filter(user__staffprofile__department=department)
    if location:
        leaves = leaves.filter(user__staffprofile__location=location)

    for leave in leaves.select_related('type'):
        for date in [d for d in leave.dates() if d in days and is_working_day(d, leave.user.staffprofile.location)]:
            days[date]['events'].append(leave)


