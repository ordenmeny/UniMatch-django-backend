import os
from time import sleep

from celery import Celery, shared_task
from djangoProject.settings import CELERY

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('proj')

app.config_from_object(CELERY)

app.autodiscover_tasks()  # для нахождения shared_task


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    return 1


@app.task(bind=True)
def very_long_task(self):
    sleep(60)
    return 1

# @app.task(
#     bind=True,
#     max_retries=5,  # Максимальное количество повторных попыток
#     default_retry_delay=60  # задержка между попытками.
#     retry_backoff=True  # Включение экспоненциального отсупа.
#     retry_backoff_max=600 # максимальное время ожидания
#     retry_jitter=True # Случайный разброс по времени
#     autoretry_for=(ValueError, )
#     acks_late=True,               # Подтверждать задачу только после успешного выполнения
#     reject_on_worker_lost=True,   # Возвращать задачу в очередь при сбое воркера
#     soft_time_limit=10 # максимальное время выполнения программы
# )
# def task(self):
#     try:
#         # if ...
#             raise
#     except ValueError as e:
#         raise self.retry(exc=e)

# Для периодических задач.
# app.conf.beat_schedule = {
#     'very_long_task': {
#         'task': 'djangoProject.celery.very_long_task',
#         'schedule': 10.0,
#     }
# }

# @shared_task
# def ad(x, y):
#     return x + y