import os
from celery import Celery
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send_weekly_articles': {
        'task': 'news.tasks.send_weekly_articles',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
