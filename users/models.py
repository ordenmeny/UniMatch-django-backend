from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.IntegerField(verbose_name="Возраст", null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    uniq_code = models.CharField(max_length=50, null=True, blank=True)
    chat_id = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="users/", null=True, blank=True)
    hobby = models.ManyToManyField("HobbyModel", verbose_name="Хобби", blank=True)


class HobbyModel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Хобби"
        verbose_name_plural = "Хобби"