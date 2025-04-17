from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eoy_platform.settings')

# Create Celery app
app = Celery('eoy_platform')

# Load settings from Django settings file
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()

# Periodic tasks schedule
app.conf.beat_schedule = {
    'monitor-gpu-every-minute': {
        'task': 'gpu_monitor.gpu_tasks.monitor_gpu_usage',  # <== Corrected task path
        'schedule': crontab(minute='*/1'),
    },
    'billing-check-every-hour': {
        'task': 'gpu_monitor.gpu_tasks.check_and_report_resource_usage',  # <== Corrected task path
        'schedule': crontab(minute=0, hour='*/1'),
    },
}
