from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from collections import OrderedDict
from .forms import *
from .signals import calendar_display
import calendar


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'staff/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        days = OrderedDict()

        today = timezone.now().date()
        year = self.kwargs.get('year', today.year)
        month = self.kwargs.get('month', today.month)
        first_day_of_month = today.replace(day=1, month=month, year=year)
        last_day_of_month = first_day_of_month.replace(day=calendar.monthrange(year, month)[1])
        first_day_of_calendar = first_day_of_month - timedelta(days=first_day_of_month.weekday())
        last_day_of_calendar = last_day_of_month + timedelta(days=6 - last_day_of_month.weekday())
        context['today'] = today
        context['weeks'] = list()
        current_date = first_day_of_calendar
        current_week = list()
        while current_date <= last_day_of_calendar:
            calendar_day = {'date': current_date, 'events' : [] }
            days[current_date] = calendar_day
            current_week.append(calendar_day)
            if len(current_week) == 7:
                context['weeks'].append(current_week)
                current_week = list()
            current_date = current_date + timedelta(days=1)
        months = list()
        if last_day_of_calendar.month >= first_day_of_calendar.month:
            months = list(range(first_day_of_calendar.month, last_day_of_calendar.month + 1))
        else: #Corner case donde pillamos diciembre+enero+ por ejemplo
            months = list(range(first_day_of_calendar.month, 12 + 1)) + list(range(1, last_day_of_calendar.month + 1))
        for birthday in Birthday.objects.filter(birthday__month__in=months, user__is_active=True).select_related('user'):
            for y in range(first_day_of_calendar.year, last_day_of_calendar.year + 1):
                birthday.birthday = birthday.birthday.replace(year=y)
                if birthday.birthday in days:
                    days[birthday.birthday]['events'].append(birthday)
        context['previous_month'] = first_day_of_month - timedelta(days=1)
        context['current_month'] = first_day_of_month
        context['next_month'] = last_day_of_month + timedelta(days=1)
        form = CalendarFilterForm(self.request.GET)
        context['form'] = form
        if form.is_valid():
            calendar_display.send(sender=self.__class__, days=days, months=months,
                department=form.cleaned_data['department'], location=form.cleaned_data['location'])
        else:
            calendar_display.send(sender=self.__class__, days=days, months=months, department=None, location=None)
        return context
