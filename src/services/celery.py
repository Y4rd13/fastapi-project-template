from __future__ import absolute_import
from celery import Celery
from src.core.logger_func import logger
from core.config import settings

celery_app = Celery(
    "celery_app",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    worker_log_format="[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s",
    worker_task_log_format="[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s",
    task_track_started=True,
    task_ignore_result=False,
    broker_connection_retry_on_startup=True
)

logger.info("Celery worker initialized.")

@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))