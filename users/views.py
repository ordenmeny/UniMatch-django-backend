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

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = PairsModel.objects.all()
        return context


class GeneratePairsAPIView(CreateAPIView):
    serializer_class = PairsSerializer

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
