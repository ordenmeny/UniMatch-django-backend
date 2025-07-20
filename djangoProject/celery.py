import os

from celery import Celery
from django.conf import settings
from time import sleep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")

app = Celery("proj")

# Детекция: запушено ли сейчас тестирование
# TESTING = 'test' in sys.argv
# TESTING = TESTING or 'test_coverage' in sys.argv or 'pytest' in sys.modules
CELERY = {
    "broker_url": "redis://localhost:6379/0",
    # 'task_always_eager': TESTING,
    "timezone": settings.TIME_ZONE,
    "result_backend": "django-db",
    "result_extended": True,
    'task_track_started': True,
}


app.config_from_object(CELERY)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

# acks_late - задача подтверждается только после успешного выполнения.
# reject_on_worker_lost - если воркер умер до ack, задача отклоняется и возвращается в очередь.
@app.task(bind=True, acks_late=True, reject_on_worker_lost=True)
def very_long_task(self):
    sleep(60)
    return 1


# app.conf.beat_schedule = {
#     'very_long_task': {
#         'task': 'djangoProject.celery.very_long_task',
#         'schedule': 10.0, # Каждые 10 секунд
#     }
# }
