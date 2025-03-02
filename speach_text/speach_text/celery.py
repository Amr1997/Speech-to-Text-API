import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'speach_text.settings')

app = Celery('speach_text')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
