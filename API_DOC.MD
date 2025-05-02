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
GET: users/api/tags/
Токен пользователя:
Authorization: Bearer <access_token>
Ответ (статус 200):
[
    "Программирование",
    "Спорт",
    "Музыка"
]

4) Получение списка тэгов:
GET: users/api/hobby/all
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