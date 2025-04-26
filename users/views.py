from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, \
    CreateAPIView, ListCreateAPIView, ListAPIView

from djangoProject import settings
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
import uuid
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.views.generic import TemplateView, ListView
from .models import *
from users.utils.generate_pairs import generate_weekly_pairs
from users.utils.check_sign import check_telegram_auth
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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
        # В БД сохраняется данные пользователя.
        # Создается токен для нового пользователя.
        # Возвращаются данные пользователя, токен.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()

        # Создаем токен для нового пользователя
        token, created = Token.objects.get_or_create(user=user)

        # Возвращаем данные пользователя и токен
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class GeneratePairsAPIView(ListCreateAPIView):
    serializer_class = PairsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        pairs = PairsModel.objects.filter(
            is_archived=True
        ).filter(
            models.Q(user1=user) | models.Q(user2=user) | models.Q(user3=user)
        ).order_by('-created_at')

        serializer = self.get_serializer(pairs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        all_pairs = PairsModel.objects.all()

        # Изменяем у всех объектов на is_archived=True.
        PairsModel.objects.all().update(is_archived=True)

        # Генерируем пары. Получаем список из пар (pairs).
        all_users = CustomUser.objects.all()
        # if (len(all_users)-1) % 2 == 0:
        #     # Если количество пользователей четное без спец.пользователя reserve-user,
        #     # то этого пользователя не учитываем

        past_pairs = set()
        for pair in PairsModel.objects.filter(is_archived=True):
            users = [u for u in [pair.user1, pair.user2, pair.user3] if u is not None]
            past_pairs.add(frozenset(users))

        pairs = generate_weekly_pairs(all_users, past_pairs)

        # Поочередно через цикл добавляем пары в БД (модель PairsModel) is_archived=False.
        for i in pairs:
            if len(i) == 2:
                PairsModel.objects.create(user1=i[0], user2=i[1], is_archived=False)
            elif len(i) == 3:
                PairsModel.objects.create(user1=i[0], user2=i[1], user3=i[2], is_archived=False)

        # [(<CustomUser: user6>, <CustomUser: user9>), (<CustomUser: admin>, <CustomUser: user7>, <CustomUser: user8>)]

        formatted_pairs = []
        for pair in pairs:
            if len(pair) == 2:
                formatted_pairs.append(
                    [pair[0].id, pair[1].id],
                )
            elif len(pair) == 3:
                formatted_pairs.append(
                    [pair[0].id, pair[1].id, pair[2].id],
                )

        return Response({
            "pairs": formatted_pairs
        }, status=status.HTTP_201_CREATED)


# Перед использованием:
# Зайти в botfather, выбрать бота, отправить хост.
@method_decorator(csrf_exempt, name='dispatch')
class TgAuthView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        if not check_telegram_auth(data, settings.TELEGRAM_BOT_TOKEN):
            return HttpResponseBadRequest("Invalid auth")

        chat_id = data.get("id", "")
        email = data.get("email", "")

        # Здесь же осуществлять логику добавления chat_id...
        user_by_email = CustomUser.objects.get(email=email)
        if user_by_email:
            user_by_email.chat_id = chat_id
            user_by_email.save()

        return Response({'user_data': data}, status=status.HTTP_201_CREATED)


class HobbyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        hobbies = request.user.hobby.all().values_list('name', flat=True)
        return Response(list(hobbies), status=status.HTTP_200_OK)