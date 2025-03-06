from celery import Celery
from django.conf import settings

# Configure Celery for GPU processing
app = Celery('transcription')

# Optimize settings for GPU processing
app.conf.update(
    # Reduce worker concurrency for GPU tasks
    worker_concurrency=2,
    
    # Enable task acknowledgment after completion
    task_acks_late=True,
    
    # Increase time limits for large-v3 model processing
    task_time_limit=1800,        # 30 minutes
    task_soft_time_limit=1500,   # 25 minutes
    
    # Optimize broker pool for GPU tasks
    broker_pool_limit=4,
    
    # Reduce prefetch to prevent GPU memory overload
    worker_prefetch_multiplier=1,
    
    # Queue configuration
    task_default_queue='transcription',
    task_queues={
        'transcription': {
            'exchange': 'transcription',
            'routing_key': 'transcription',
        },
        'gpu_tasks': {
            'exchange': 'gpu_tasks',
            'routing_key': 'gpu_tasks',
        }
    },
    
    # Route tasks to GPU queue
    task_routes={
        'transcription.tasks.process_audio': {'queue': 'gpu_tasks'}
    },
    
    # Optimize for long-running GPU tasks
    broker_transport_options={
        'visibility_timeout': 3600,  # 1 hour
    }
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)