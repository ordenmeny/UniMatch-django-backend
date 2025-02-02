from django.urls import path
from .views import *
from .api_views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('get-bot/', GetBotView.as_view()),
    path('api/get-bot/<slug:uniq_code>/', GetUserAPIView.as_view()),
]
