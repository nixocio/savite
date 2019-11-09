import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_app.settings")

celery_app = Celery("web_app")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "check-expiration-daily": {
        "task": "deadline_expired",
        "schedule": crontab(minute="*"),
    }
}
