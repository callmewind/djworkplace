from django.urls import path
from .views import *

app_name = 'holidays'

urlpatterns = [
   path('create/', CreateHoliday.as_view(), name='create'),
]