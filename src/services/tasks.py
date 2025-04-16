from __future__ import absolute_import, unicode_literals
from celery import shared_task
from services.celery import celery_app
#from core.logger_func import logger
from core.config import settings
#from celery.utils.log import get_task_logger

#logger = get_task_logger(__name__)

# @shared_task(name="chat_task", queue="high", time_limit=30)
# def chat_task(request, messages, max_new_tokens, temperature):
#     return chat(request, messages, max_new_tokens, temperature)