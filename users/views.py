from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, \
    CreateAPIView, ListCreateAPIView, ListAPIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from djangoProject import settings
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
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
from datetime import datetime, timedelta, time
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


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
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            error_at_all = ''

            for field, messages in serializer.errors.items():
                if field == 'email':
                    for message in messages:
                        if message.code == 'unique':
                            error_at_all += 'Пользователь с таким email уже существует.'
                            break
                if field == 'password':
                    error_at_all += 'Пароль либо слишком простой, либо содержит меньше 4 символов.'
                if field == 'birth':
                    error_at_all += 'Проблема с датой.'

                if error_at_all == '':
                    error_at_all += 'Произошла непредвиденная ошибка.'

            return Response({'error': error_at_all}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.is_active = True

        user.save()
        refresh_token = RefreshToken.for_user(user)
        access = refresh_token.access_token

        response = Response({
            'user': UserSerializer(user).data,
            'access': str(access)
        }, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=False,  # change on https
            samesite='Lax',
            max_age=24 * 60 * 60,
        )

        return response


class CurrentPairAPIView(APIView):
    serializer_class = UserSerializer

    # Получение пары текущего пользователя
    def get(self, request, *args, **kwargs):
        user = self.request.user

        cur_pair = PairsModel.objects.filter(is_archived=False).filter(
            models.Q(user1=user) | models.Q(user2=user) | models.Q(user3=user)
        )


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

        cur_pair = PairsModel.objects.filter(
            is_archived=False
        ).filter(
            models.Q(user1=user) | models.Q(user2=user) | models.Q(user3=user)
        ).order_by('-created_at').first()

        all_pairs = list(pairs)
        if cur_pair:
            all_pairs.insert(0, cur_pair)


        serializer = self.get_serializer(pairs, many=True)

        return Response({
            'current_pair': self.get_serializer(cur_pair).data if cur_pair else None,
            'pairs': serializer.data
        })

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

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = HobbyUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_hobbies = serializer.validated_data["hobby"]
        user.hobby.set(new_hobbies)
        user.save()

        return Response(new_hobbies, status=status.HTTP_200_OK)


class HobbyAllAPIView(ListAPIView):
    queryset = HobbyModel.objects.all()
    serializer_class = HobbySerializer
    permission_classes = [AllowAny]


class DaysToMatch(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        now = datetime.now()

        # День недели мэтча (0 = Понедельник, 1 = Вторник, ..., 6 = Воскресенье)
        day_of_week_match = 0

        # Время мэтча
        match_time = time(10, 0)  # 10:00 утра

        # Сколько дней до следующего мэтча
        days_ahead = (day_of_week_match - now.weekday()) % 7
        if days_ahead == 0:
            # Сегодня день мэтча, но надо проверить время
            if now.time() >= match_time:
                days_ahead = 7  # Уже позже 10:00 — ждём следующий понедельник

        next_match_datetime = datetime.combine(now.date() + timedelta(days=days_ahead), match_time)

        # Разница между сейчас и следующим мэтчем
        delta = next_match_datetime - now

        response_data = {
            'days_left': delta.days,
            'hours_left': delta.seconds // 3600,
            'minutes_left': (delta.seconds % 3600) // 60,
            'next_match_at': next_match_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class HobbyTotal(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        user_tags = user.hobby.all()
        all_tags = HobbyModel.objects.all()

        user_tags_data = [{'id': tag.id, 'name': tag.name} for tag in user_tags]
        all_tags_data = [{'id': tag.id, 'name': tag.name} for tag in all_tags]

        response_data = {
            'user_tags': user_tags_data,
            'all_tags': all_tags_data
        }

        return Response(response_data)


class UpdateUserAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response({'error': 'Неверный email или пароль'}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        refresh_token = validated_data.pop('refresh')
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,  # change on https
            samesite='Lax',
            max_age=24 * 60 * 60,
        )

        return response


class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'error': 'Необходимо пройти авторизацию'},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'error': 'Необходимо пройти авторизацию'}, status=status.HTTP_401_UNAUTHORIZED)

        access = serializer.validated_data.get('access')
        new_refresh = serializer.validated_data.get('refresh')

        response = Response({'access': access}, status=status.HTTP_200_OK)
        if new_refresh:
            response.set_cookie(
                key='refresh_token',
                value=new_refresh,
                httponly=True,
                secure=False,  # change on https
                samesite='Lax',
                max_age=24 * 60 * 60,
            )

        return response
