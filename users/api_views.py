from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from rest_framework.permissions import IsAdminUser


class GetUserAPIView(RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]

    # lookup_field указывает, по какому полю модели будет производиться поиск объекта.
    lookup_field = 'uniq_code'
    # lookup_url_kwarg указывает на поле из url, по которому будет вестись поиск.
    lookup_url_kwarg = 'uniq_code'
