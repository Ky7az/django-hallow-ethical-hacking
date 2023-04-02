import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoHallowEthicalHacking.settings')
app = Celery('DjangoHallowEthicalHacking')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scrap-feeds-every-hour': {
        'task': 'HallowWatch.tasks.scrap_feeds',
        'schedule': crontab(hour='*/1')
    }
}
