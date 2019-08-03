from django.urls import path
from .views import *

app_name = 'holidays'

urlpatterns = [
   path('request_leave/', RequestLeave.as_view(), name='request-leave'),
]