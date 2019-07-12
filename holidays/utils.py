from django.core.cache import cache
from django.db.models import Q

def location_holidays_key(year, location): return 'location-holidays-%d-%d' % (year, location.pk)

def holidays_key(year): return 'holidays-%d' % year

def holidays(year):
    from .models import PublicHoliday
    return PublicHoliday.objects.filter(Q(yearly=True)|Q(date__year=year)).prefetch_related('locations')
    
def location_holiday_dates(year, location):
    location_holidays = (
        h for h in cache.get_or_set(holidays_key(year), lambda: list(holidays(year)))
        if location in h.locations.all() or not len(h.locations.all())
    )
    return (
        h.date.replace(year=year) if h.yearly else h.date
        for h in location_holidays
    )

def is_working_day(date, location):
    year = date.year
    dates = cache.get_or_set(location_holidays_key(year, location), lambda: list(location_holiday_dates(year, location)))
    return date.weekday() < 5 and date not in dates