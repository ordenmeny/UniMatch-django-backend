from celery import shared_task
import logging

from django.contrib.auth import get_user_model

from .models import *

logger = logging.getLogger(__name__)

@shared_task
def my_scheduled_task():
    users = get_user_model().objects.all()[:3]

    pair = PairsModel.objects.create(
        user1=users[0],
        user2=users[1],
        user3=users[2],
        is_archived=True
    )
    pair.save()
    logger.info(f"✅ Создана пара")
