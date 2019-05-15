from holidays.models import *
from datetime import timedelta
from django.db import transaction
from django.db.models.signals import post_save
from staff.signals import calendar_display
from staff.views import CalendarView
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

@receiver(post_save, sender=Vacation)
def onVacationsRequest(sender, instance, created, **kwargs):
    if created and not instance.approval_date:
        from djworkplace.tasks import enqueue_mail
        transaction.on_commit(lambda: enqueue_mail(
                _('Vacations request'),
                _("%s is requesting a vacation period from %s to %s") % (instance.user, instance.start, instance.end),
                [manager.email for manager in instance.user.staffprofile.department.managers.all()]
            )
        )

@receiver(calendar_display, sender=CalendarView)
def on_calendar_display(sender, days, department, location, **kwargs):
    day_list = list(days.keys())
    first_day_of_calendar = next(iter(day_list))
    last_day_of_calendar = next(reversed(day_list)) 

    public_holidays = PublicHoliday.objects.filter(
        Q(date__gte=first_day_of_calendar, date__lte=last_day_of_calendar))
    if location:
        public_holidays = public_holidays.filter(Q(location__isnull=True)|Q(location=location))
    for holiday in public_holidays:
        days[holiday.date]['events'].append(holiday)


    vacations = Vacation.objects.filter(Q(start__range=(first_day_of_calendar, last_day_of_calendar))|Q(end__range=(first_day_of_calendar, last_day_of_calendar)))
    if department:
        vacations = vacations.filter(user__staffprofile__department=department)
    if location:
        vacations = vacations.filter(user__staffprofile__location=location)

    for vacation in vacations:
        day = max(vacation.start, first_day_of_calendar)
        while day <= min(vacation.end, last_day_of_calendar):
            days[day]['events'].append(vacation)
            day = day + timedelta(days=1)



