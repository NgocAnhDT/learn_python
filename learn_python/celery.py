from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_python.settings')

app = Celery('learn_python')

app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'add-ten-seconds': {
        'task': 'add',
        'schedule': 10.0,
        'args': (1, 2)
    },
    'count-user-sixty-seconds': {
        'task': 'count_user',
        'schedule': 60.0
    },
    'rename-user-sixty-seconds': {
        'task': 'rename_user',
        'schedule': 60.0,
        'args': (1, 'Ha')
    },
    'update-status-ten-seconds': {
        'task': 'update_status',
        'schedule': 10.0
    },
}
