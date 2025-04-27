from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from djoser.serializers import TokenSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'age', 'chat_id', 'image', 'hobby', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Метод, который срабатывает при регистрации пользователя
        validated_data['username'] = validated_data['email']
        password = validated_data.pop('password')  # Извлекаем пароль
        user = super().create(validated_data)  # Создаем пользователя
        user.set_password(password)  # Хешируем пароль
        user.save()  # Сохраняем пользователя с хешированным паролем

        return user


class PairsSerializer(serializers.ModelSerializer):
    partner = serializers.SerializerMethodField()

    def get_partner(self, obj):
        partner = None
        current_user = self.context['request'].user

        if obj.user1 and obj.user1 != current_user:
            partner = obj.user1
        if obj.user2 and obj.user2 != current_user:
            partner = obj.user2
        if obj.user3 and obj.user3 != current_user:
            partner = obj.user3

        partner_data = {
            'id': partner.id,
            'first_name': partner.first_name,
            'last_name': partner.last_name,
            'email': partner.email
        }

        return partner_data

    class Meta:
        model = PairsModel
        fields = ['id', 'partner', 'created_at']


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = HobbyModel
        fields = "__all__"

    # def to_representation(self, instance):
    #     return {"name": instance}


class CustomTokenSerializer(TokenSerializer):
    class Meta(TokenSerializer.Meta):
        fields = ('key', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'token': representation['key']
        }

