from celery import Celery
from django.conf import settings

# Configure Celery for parallel processing
app = Celery('transcription')

app.conf.update(
    worker_concurrency=10,
    task_acks_late=True,
    task_time_limit=600,
    task_soft_time_limit=540,
    broker_pool_limit=10,
    worker_prefetch_multiplier=1,
    task_default_queue='transcription',
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)