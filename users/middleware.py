from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class TokenRefreshMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        refresh_token = request.COOKIES.get('refresh_token')


        # Проверяем, есть ли access-токен
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        access_token = auth_header.split(' ')[1]

        try:
            token = AccessToken(access_token)
            return None
        except:
            token = None

        if not refresh_token:
            return JsonResponse({"error": "Неверный токен, пройдите авторизацию"},
                                status=401)

        try:
            refresh = RefreshToken(refresh_token)
        except:
            return JsonResponse({"error": "Неверный токен, пройдите авторизацию"},
                                status=401)

        # Обновление access-токена
        new_access = str(refresh.access_token)

        # Обновление refresh-токена
        # .....

        # Заносим refresh в httponly
        # .....




        # except Exception:
        #     if not refresh_token:
        #         return JsonResponse({"error": "Неверный токен, пройдите авторизацию"},
        #                             status=401)
        #     try:
        #         refresh = RefreshToken(refresh_token)
        #         new_access = str(refresh.access_token)
        #         print(new_access, '!!!')
        #
        #         new_refresh = str(RefreshToken.for_user(refresh.user))
        #
        #         request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access}'
        #
        #         def set_cookies(response):
        #             # Устанавливаем новый access-токен
        #             response.set_cookie(
        #                 'access_token',
        #                 new_access,
        #                 httponly=True,
        #                 secure=True,
        #                 samesite='Strict',
        #                 max_age=5 * 60  # 5 минут
        #             )
        #
        #             # Устанавливаем новый refresh-токен
        #             response.set_cookie(
        #                 'refresh_token',
        #                 new_refresh,
        #                 httponly=True,
        #                 secure=True,
        #                 samesite='Strict',
        #                 max_age=14 * 24 * 60 * 60  # 14 дней
        #             )
        #
        #             return response
        #
        #         # Добавляем обработчик в запрос, чтобы можно было применить в view
        #         request.set_cookie_on_response = set_cookies
        #
        #
        #     except Exception:
        #         return JsonResponse({"error": "Invalid refresh token. Please log in again."}, status=401)
