from django.contrib.auth.models import AbstractUser
from django.db import models


class PairsModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    user1 = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="user2")
    user3 = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="user3", null=True, default=None, blank=True)
    is_archived = models.BooleanField(null=True, blank=True)  # Если True - пара уже была

    def __str__(self):
        return f'{self.user1} - {self.user2}'


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
