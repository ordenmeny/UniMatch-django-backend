from celery import shared_task
from time import sleep
import logging

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True
)
def make_pairs(self):
    for i in range(50):
        sleep(0.1)
        logger.info(f"New pair: user{i+1} and user{i+2}")
    return 1
