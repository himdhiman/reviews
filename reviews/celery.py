from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from datetime import timedelta
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviews.settings")

app = Celery("reviews")
app.conf.enable_utc = False

app.conf.update(timezone=settings.TIME_ZONE)

app.config_from_object(settings, namespace="CELERY")


# Celery Beat Settings
app.conf.beat_schedule = {
    "sync-database-with-product-and-sku": {
        "task": "main.tasks.syncProductIdAndName",
        "schedule": crontab(minute=0, hour=0),
    },
    "tracking-list-cleanup-and-push-data": {
        "task": "main.tasks.cleanReviews",
        "schedule": timedelta(hours=settings.TRACKINGLIST_CLEANUP_INTERVAL),
    },
}


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
