import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoHallowEthicalHacking.settings')
app = Celery('DjangoHallowEthicalHacking')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
