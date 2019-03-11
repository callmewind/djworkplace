from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
import calendar


class CalendarView(TemplateView):
	template_name = 'calendar.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		today = timezone.now().date()
		year = self.kwargs.get('year', today.year)
		month = self.kwargs.get('month', today.month)
		first_day_of_month = today.replace(day=1, month=month, year=year)
		last_day_of_month = first_day_of_month.replace(day=calendar.monthrange(year, month)[1])
		first_day_of_calendar = first_day_of_month - timedelta(days=first_day_of_month.weekday())
		last_day_of_calendar = last_day_of_month + timedelta(days=6 - last_day_of_month.weekday())
		context['today'] = today
		context['weeks'] = list()
		current_day = first_day_of_calendar
		current_week = list()
		while current_day <= last_day_of_calendar:
			current_week.append(current_day)
			if len(current_week) == 7:
				context['weeks'].append(current_week)
				current_week = list()
			current_day = current_day + timedelta(days=1)
		context['previous_month'] = first_day_of_month - timedelta(days=1)
		context['current_month'] = first_day_of_month
		context['next_month'] = last_day_of_month + timedelta(days=1)
		return context

