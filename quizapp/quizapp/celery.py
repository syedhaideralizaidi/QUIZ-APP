from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
# from django.conf import settings

settings = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
# settings.configure()
app = Celery('quizapp')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace = "CELERY")

#Celery Beat settings
app.conf.beat_schedule = {
    'get_task_3s':{
        'task': 'base.tasks.test_func',
        'schedule': 3.0,
    }
}
app.autodiscover_tasks()

@app.task(bind = True)
def debug_task(self):
    print({self.request})
