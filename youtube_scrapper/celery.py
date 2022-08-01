from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_scrapper.settings')

app = Celery('youtube_scrapper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scrap-youtube-channels': {
        'task': 'crawl_video',
        'schedule': 20 * 60,
    },
    'process-statistics': {
        'task': 'process_stats',
        'schedule': 20 * 60,
    },
}
