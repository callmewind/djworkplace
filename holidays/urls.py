from django.urls import path
from .views import *

app_name = 'holidays'

urlpatterns = [
   path('create_vacations/', CreateVacations.as_view(), name='create-vacations'),
]