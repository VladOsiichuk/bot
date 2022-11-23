import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('bot')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "schedule_lesson_notification": {
        "task": "apps.schedule.tasks.schedule_lessons_for_today",
        "schedule": crontab(hour=5, minute=0)
    }
}
app.conf.broker_transport_options = {'visibility_timeout': 86400}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')