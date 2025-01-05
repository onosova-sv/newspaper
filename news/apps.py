from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler import util
from .tasks import send_weekly_articles

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@util.close_old_connections
def start_scheduler():
    scheduler.add_job(
        send_weekly_articles,
        trigger='cron',
        day_of_week='mon',  # Запускать каждую неделю в понедельник
        hour=8,             # В 8 утра
        minute=0,
        id='send_weekly_articles',
        replace_existing=True,
    )
    scheduler.start()

# Вызов функции start_scheduler при запуске приложения
start_scheduler()

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        pass
        #import NewsPaper.news.signals
