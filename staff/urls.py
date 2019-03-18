from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
   path('calendar/', CalendarView.as_view(), name='calendar'),
   path('calendar/<int:year>-<int:month>/', CalendarView.as_view(), name='calendar'),
  ]