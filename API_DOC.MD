1) Регистрация:
POST users/api/register/
{
  "email": "почта@example.com",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "age": 25,
  "password": "пароль",
  "hobby": [1, 2, 5]
}

Уточнение: [1, 2, 5] - индексы хобби (тэгов)

Ответ: 
{
    "user": {
        "first_name": "Имя",
        "last_name": "Фамилия",
        "email": "user6@yandex.ru",
        "age": 25,
        "chat_id": null,
        "image": null,
        "hobby": []
    },
    "token": "10da5bde989c977c5fea1e885567a714aba05c40"
}
Сохранить token. Код успешного ответа: 201.
Если email уже существует (код ошибки: 400): 
{
    "email": [
        "user with this email already exists."
    ]
}

2) Авторизация:
POST: /auth/token/login/
{
    "email": "admin@yandex.ru",
    "password": "пароль"
}

Ответ: токен пользователя (необходимо сохранить на клиенте):
{
    "token": "b74fcf715b641e919ba2a7f9157c24d344dcf222"
}
Код успешного ответа: 201.

Код ошибки: 400
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}

3) 
Привязка в тг-боту:
POST: users/api/tg-auth/
Пример использования:
https://github.com/ordenmeny/UniMatch-django-backend/blob/main/users/templates/users/tg_auth.html
Код успешного ответа: 201.

4) Получение истории мэтчей текущего пользователя:
GET: users/api/pairs/
Токен пользователя:
Authorization: token <token>

Ответ:
[
    {
        "id": 222,
        "partner": {
            "id": 35,
            "first_name": "Александр",
            "last_name": "Кожевников",
            "email": "user4@yandex.ru"
        },
        "created_at": "2025-04-27"
    },
    {
        "id": 223,
        "partner": {
            "id": 31,
            "first_name": "Дмитрий",
            "last_name": "Александров",
            "email": "admin@yandex.ru"
        },
        "created_at": "2025-04-27"
    }
]

5) Получение списка тэгов пользователя
GET: users/api/tags/
Токен пользователя:
Authorization: token <token>
Ответ (статус 200):
[
    "Программирование",
    "Спорт",
    "Музыка"
]

6) Получение списка тэгов:
GET: users/api/hobby/all
Токен пользователя:
Authorization: token <token>
Ответ:
[
    {
        "id": 1,
        "name": "Программирование"
    },
    {
        "id": 2,
        "name": "Спорт"
    },
    {
        "id": 3,
        "name": "Рисование"
    },
    {
        "id": 4,
        "name": "Литература"
    }
]

7) Выйти из системы:
POST: auth/token/logout/

8) Дней до мэтча:
GET: users/api/days-to-match/
{
    "days_left": 1, // полных дней до
    "hours_left": 13,  // полных дней до + полных часов до
    "minutes_left": 17, // полных дней до + полных часов до + полных минут до
    "next_match_at": "2025-04-29 10:00:00"  // В общем виде дата-время след.мэтча
}