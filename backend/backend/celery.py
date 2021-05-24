from celery.schedules import crontab
import os
from celery import Celery
from django.conf import settings 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings') 

app = Celery('backend') 
app.autodiscover_tasks()

app.config_from_object('django.conf:settings') 
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) 


'''app.conf.beat_schedule = {
    # Executed every Monday at 09:00
    'hello': {
        'task': 'actions.tasks.hello',
        'schedule': 10.0,
    },
}'''