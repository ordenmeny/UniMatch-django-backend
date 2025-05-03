1) Привязка в тг-боту:
POST: users/api/tg-auth/
Пример использования:
https://github.com/ordenmeny/UniMatch-django-backend/blob/main/users/templates/users/tg_auth.html
Код успешного ответа: 201.

2) Получение истории мэтчей текущего пользователя:
GET: users/api/pairs/
Токен пользователя:
Authorization: Bearer <access_token>

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

3) Получение списка тэгов пользователя
GET: users/api/hobby/
Токен пользователя:
Authorization: Bearer <access_token>
Ответ (статус 200):
[
    "Программирование",
    "Спорт",
    "Музыка"
]

4) Получение списка тэгов:
GET: users/api/hobby/all/
Токен пользователя:
Authorization: Bearer <access_token>
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


5) Дней до мэтча:
GET: users/api/days-to-match/
{
    "days_left": 1, // полных дней до
    "hours_left": 13, // полных дней до + полных часов до
    "minutes_left": 17, // полных дней до + полных часов до + полных минут до
    "next_match_at": "2025-04-29 10:00:00" // В общем виде дата-время след.мэтча
}

6) Получение тэгов пользователя и всех тэгов в одном запросе:
GET: users/api/hobby/total/
Authorization: Bearer <access_token>

Response (OK: 200)
{
    "user_tags": [
        {
            "id": 2,
            "name": "Литература"
        },
        {
            "id": 3,
            "name": "История"
        }
    ],
    "all_tags": [
        {
            "id": 1,
            "name": "Программирование"
        },
        {
            "id": 2,
            "name": "Литература"
        },
        {
            "id": 3,
            "name": "История"
        }
    ]
}

7) Обновление тэгов:
PATCH: users/api/hobby/
Authorization: Bearer <access_token> 
{
    "hobby": [1, 2]
}

Список [1, 2] - итоговые тэги пользователя.

Response 200


1) Регистрация:
POST users/api/register/
{
  "email": "почта@example.com",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "birth": "20-01-2000",
  "password": "пароль",
  "hobby": [1, 2, 5]
}

Уточнение: [1, 2, 5] - индексы хобби (тэгов)

Ответ: 
{
    "user": {
        "first_name": "Имя",
        "last_name": "Фамилия",
        "email": "email@example.com",
        "birth": "02-03-2000",
        "chat_id": null,
        "image": null,
        "hobby": [
            1,
            2,
            5
        ]
    },
    "refresh": <refresh_token>,
    "access": <access_token> 
}
Код успешного ответа: 201.
Сохранить refresh и access токены на клиенте.

!!! change !!!
Если email уже существует (код ошибки: 400): 
{
    "email": [
        "user with this email already exists."
    ]
}

2) Авторизация:

POST: api/token/
{
    "email": "user9@yandex.ru",
    "password": "пароль"
}

Response (OK: 200): 
{
    "refresh": <refresh_token>,
    "access": "<access_token>"
}

Ошибка 401 (неверный email или пароль):
{
    "detail": "No active account found with the given credentials"
}


Необходимо сохранить refresh и access токены на клиенте.

3) Обновление access-токен:

Условие, при котором необходимо обновить access-токен:
если получен ответ с кодом 401 (при доступе к контенту и т.д), 
но refresh-токен доступен.

При запросе меняется не только access-токен, но и refresh-токен, 
поэтому на клиенте необходимо сохранить оба токена. 

POST: api/token/refresh/
{
    "refresh": <refresh_token>
}

Response (OK: 200):
{
    "access": <access_token>,
    "refresh": "<refresh_token>"
}

Если ошибка, то редирект на страницу с регистрацией.

4) Получение текущего пользователя по JWT-токену:
POST: auth/users/me/

Header:
Bearer <access_token>

Response (200):
{
    "first_name": "Имя",
    "last_name": "Фамилия",
    "email": "user9@yandex.ru",
    "birth": null,
    "chat_id": null,
    "image": null,
    "hobby": [1, 2, 3]
}

5) Выйти
Отозвать refresh-токен и удалить access-токен на клиенте.
POST: api/token/blacklist/
{
    "refresh": "<refresh_token>"
}
   
Response: 200