from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, \
    CreateAPIView
from .serializers import *
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
import uuid
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.views.generic import TemplateView, ListView
from .models import *
from users.utils.generate_pairs import generate_weekly_pairs

class GenerateUniqCodeAPIView(APIView):
    def get(self, request):
        uniq_code = str(uuid.uuid4())

        return Response({'uniq_code': uniq_code})


class UserByUniqCodeAPIView(RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uniq_code'
    lookup_url_kwarg = 'uniq_code'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        token, created = Token.objects.get_or_create(user=instance)

        serializer = self.get_serializer(instance)

        return Response({
            "user": serializer.data,
            "token": token.key
        })


class UserByChatIDAPIView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'chat_id'
    lookup_url_kwarg = 'chat_id'
    permission_classes = [IsAdminUser]


class RegisterUserAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Метод для регистрации пользователя через API (POST-запрос).
        # В БД сохраняется только uniq_code и введенные данные пользователя.
        # Создается токен для нового пользователя.
        # Возвращаются данные пользователя, токен, uniq_code.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()

        uniq_code = str(uuid.uuid4())
        user.uniq_code = uniq_code
        user.save()

        # Создаем токен для нового пользователя
        token, created = Token.objects.get_or_create(user=user)

        # Возвращаем данные пользователя и токен
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'uniq_code': uniq_code
        }, status=status.HTTP_201_CREATED)


class ConfirmPairsView(TemplateView):
    template_name = 'users/pairs.html'

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CurrentPairsModel.objects.all()
        print(context['users'])
        return context

class GeneratePairsAPIView(CreateAPIView):
    pass

