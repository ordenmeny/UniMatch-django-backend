from django.urls import path, re_path, include
from django.views.generic import TemplateView
from .models import *
from .views import *

app_name = "users"

urlpatterns = [
    path('api/register/', RegisterUserAPIView.as_view()),
    path('api/update/user/', UpdateUserAPIView.as_view()),
    # Все запросы для работы с пользователями по chat_id.
    path('api/user-by-chat-id/<str:chat_id>/', UserByChatIDAPIView.as_view()),

    path('api/pairs/', GeneratePairsAPIView.as_view()),
    path('api/current/pair', CurrentPairAPIView.as_view()),
    path('api/tg-auth/', TgAuthView.as_view()),
    path('api/hobby/', HobbyAPIView.as_view()),
    path('api/hobby/all/', HobbyAllAPIView.as_view()),
    path('api/days-to-match/', DaysToMatch.as_view()),
    path('api/hobby/total/', HobbyTotal.as_view()),
    path('api/token/refresh/', RefreshTokenView.as_view()),
    # not api
    path('tg-btn-auth/', TemplateView.as_view(template_name='users/tg_auth.html')),
]
