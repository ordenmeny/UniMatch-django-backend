from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')  # Извлекаем пароль
        user = super().create(validated_data)  # Создаем пользователя
        user.set_password(password)  # Хешируем пароль
        user.save()  # Сохраняем пользователя с хешированным паролем
        
        return user

