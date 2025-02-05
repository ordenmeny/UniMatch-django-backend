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
    path('api/get-bot/<slug:uniq_code>/', SetUserBotAPIView.as_view()),
    path('api/get-user/<str:chat_id>/', GetUserAPIView.as_view()),
])
