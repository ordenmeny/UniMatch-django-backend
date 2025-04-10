from django.urls import path
from django.views.generic import TemplateView
from .models import *
from .views import *

app_name = "users"

urlpatterns = [
    # Регистрация пользователя через API (POST-запрос).
    path('api/register/', RegisterUserAPIView.as_view()),

    # Все запросы для работы с пользователями по uniq_code.
    path('api/user-by-uniq-code/<str:uniq_code>/', UserByUniqCodeAPIView.as_view()),

    # Все запросы для работы с пользователями по chat_id.
    path('api/user-by-chat-id/<str:chat_id>/', UserByChatIDAPIView.as_view()),

    # Клиенту необходимо сделать GET-запрос и получить uniq_code 
    # для формирования ссылки на бота в таком виде: https://t.me/Uni_Match_Bot?start=login_`uniq_code`
    path('api/generate-uniq-code/', GenerateUniqCodeAPIView.as_view()),

    # 1) Делаем запрос на формирование пар.
    # 2) Пары из CurrentPairsModel удаляются, но добавляются в HistoryPairsModel
    # 3) Эти пары добавляются в модель CurrentPairsModel
    # 4) На выход получаем пары из CurrentPairsModel.
    path('api/generate-pairs/', GeneratePairsAPIView.as_view()),
    path('confirm-pairs/', ConfirmPairsView.as_view()),
]
