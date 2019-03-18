from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .forms import *
import calendar



class CalendarView(TemplateView):
	template_name = 'calendar.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		days = {}

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
		context['previous_month'] = first_day_of_month - timedelta(days=1)
		context['current_month'] = first_day_of_month
		context['next_month'] = last_day_of_month + timedelta(days=1)
		form = CalendarFilterForm(self.request.GET)
		context['form'] = form

		from holidays.models import Holiday
		holidays = Holiday.objects.filter(Q(start__range=(first_day_of_calendar, last_day_of_calendar))|Q(end__range=(first_day_of_calendar, last_day_of_calendar)))
		if form.is_valid():
			if form.cleaned_data['department']:
				holidays = holidays.filter(user__staffprofile__department=form.cleaned_data['department'])
			if form.cleaned_data['location']:
				holidays = holidays.filter(user__staffprofile__location=form.cleaned_data['location'])

		for holiday in holidays:
			day = max(holiday.start, first_day_of_calendar)
			while day <= min(holiday.end, last_day_of_calendar):
				days[day]['events'].append(holiday)
				day = day + timedelta(days=1)

		return context

