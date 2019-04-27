import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djworkplace.settings')

app = Celery('djworkplace')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from .tasks import *