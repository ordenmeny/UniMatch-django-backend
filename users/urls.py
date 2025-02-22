from django.urls import path
from .views import *
from .api_views import *

app_name = "users"

urlpatterns = [
    path('login/', CustomLoginView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('get-bot/', GetBotView.as_view(), name="get_bot"),
]

urlpatterns.extend([
    # Регистрация пользователя через API (POST-запрос).
    path('api/register-user/', RegisterUserAPIView.as_view()),

    # Все запросы для работы с пользователями по uniq_code.
    path('api/get-user-by-uniq-code/<str:uniq_code>/', GetUserByUniqCodeAPIView.as_view()),

    # Все запросы для работы с пользователями по chat_id.
    path('api/get-user-by-chat-id/<str:chat_id>/', GetUserByChatIDAPIView.as_view()),

    # Генерация uniq_code для ссылки на бота, uniq_code сохраняется в сессии браузера.
    # Клиенту необходимо сделать GET-запрос и получить uniq_code 
    # для формирования ссылки на бота в таком виде: https://t.me/Uni_Match_Bot?start=login_`uniq_code`
    path('api/generate-uniq-code/', GenerateUniqCodeAPIView.as_view()),

    # Проверка на сходство uniq_code из сессии браузера и uniq_code из БД.
    # path('api/check-similarity-uniq-code/', CheckSimilarityUniqCode.as_view()),

])