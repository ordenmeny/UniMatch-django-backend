from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from rest_framework.permissions import IsAdminUser


class SetUserBotAPIView(RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uniq_code'
    lookup_url_kwarg = 'uniq_code'


class GetUserAPIView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'chat_id'
    lookup_url_kwarg = 'chat_id'
    permission_classes = [IsAdminUser]

