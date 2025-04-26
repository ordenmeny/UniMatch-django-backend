1) Регистрация:
POST users/api/register/
{
  "email": "почта@example.com",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "age": 25,
  "password": "пароль"
}


Ответ: Код успешного ответа: 201.

2) Авторизация:
POST: /auth/token/login/
{
    "username": "admin@yandex.ru",
    "password": "пароль"
}

В хедере запроса необходимо передавать токен администратора:
Authorization: token <admin_token>

Ответ: токен пользователя (необходимо сохранить на клиенте):
{
    "auth_token": "b74fcf715b641e919ba2a7f9157c24d344dcf222"
}
Код успешного ответа: 201.
Авторизацию нужно производить сразу после авторизации.

3) 
Привязка в тг-боту:
POST: users/api/tg-auth/
Пример использования:
https://github.com/ordenmeny/UniMatch-django-backend/blob/main/users/templates/users/tg_auth.html
Код успешного ответа: 201.

4) Получение истории мэтчей текущего пользователя:
GET: users/api/pairs/
Токен пользователя:
Authorization: token <auth_token>

Ответ:
[
    {
        "id": 210,
        "users": [
            "Дмитрий Александров",
            "Дмитрий Побединский",
            "Арсений Петров"
        ],
        "created_at": "2025-04-11",
        "is_archived": true,
        "user1": 31,
        "user2": 36,
        "user3": 37
    },
    ...
]

5) Получение списка тэгов (названия тэгов)
POST: users/api/tags/
Токен пользователя:
Authorization: token <auth_token>
Ответ (статус 200):
[
    "Программирование",
    "Спорт",
    "Музыка"
]