## API документация

### Регистрация

```
  POST users/api/register/
```

```http 
{
  "email": "почта@example.com",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "birth": "20-01-2000",
  "password": "пароль",
  "hobby": [1, 2, 5]
}
```

Уточнение: [1, 2, 5] - индексы хобби (тэгов)

Response (status 201):

```http
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
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```

Сохранить refresh и access токены на клиенте.

Response (status 400):
{
    "email": [
        "пользователь с таким email уже существует."
    ],
    "birth": [
        "Неправильный формат даты."
    ],
    "password": [
        "Введённый пароль слишком короткий. Он должен содержать как минимум 4 символа."
    ]
}


### Авторизация

```
  POST api/token/
```

```http
  {
    "email": "user9@yandex.ru",
    "password": "пароль"
  }
```

Response (status 200): 
```http
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
```
Необходимо сохранить refresh и access токены на клиенте.

Ошибка 401 (неверный email или пароль):
```http
{
    "detail": "No active account found with the given credentials"
}
```


### Обновление access-токен

Условие, при котором необходимо обновить access-токен:
если получен ответ с кодом 401 (при доступе к контенту и т.д), 
но refresh-токен доступен.

При запросе меняется не только access-токен, но и refresh-токен, поэтому на клиенте необходимо сохранить оба токена. 

```
POST: api/token/refresh/
```

```http
{
    "refresh": "<refresh_token>"
}
```


Response (status 200):
```http
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

Если ошибка, то редирект на страницу с авторизацией.


### Получение текущего пользователя по JWT-токену

```
POST: auth/users/me/
```

```http
Authorization: Bearer <access_token>
```

Response (200):
```
{
    "first_name": "Имя",
    "last_name": "Фамилия",
    "email": "user9@yandex.ru",
    "birth": null,
    "chat_id": null,
    "image": null,
    "hobby": [1, 2, 3]
}
```

### Выйти
Отозвать refresh-токен и удалить access-токен на клиенте.
```
POST: api/token/blacklist/
```
```
{
    "refresh": "<refresh_token>"
}
```
   
Response: 200


### Привязка в тг-боту
```
POST: users/api/tg-auth/
```
Пример использования:
[Пример](https://github.com/ordenmeny/UniMatch-django-backend/blob/main/users/templates/users/tg_auth.html)

Код успешного ответа: 201.


### Получение истории мэтчей текущего пользователя:
```
GET: users/api/pairs/
```
```
Authorization: Bearer <access_token>
```

Response (status 200):
```
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
```

### Получение списка тэгов пользователя
```
GET: users/api/hobby/
```
```
Authorization: Bearer <access_token>
```

Response (status 200):
[
    "Программирование",
    "Спорт",
    "Музыка"
]


### Получение списка тэгов
```
GET: users/api/hobby/all/
```
```
Authorization: Bearer <access_token>
```
Response (status 200):
```
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
```

### Получение тэгов пользователя и всех тэгов в одном запросе
```
GET: users/api/hobby/total/
```
```
Authorization: Bearer <access_token>
```

Response (status 200)
```
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
```

### Обновление тэгов
```
PATCH: users/api/hobby/
```
```
Authorization: Bearer <access_token> 
```
```
{
    "hobby": [1, 2]
}
```

Список [1, 2] - итоговые тэги пользователя.

Response: status 200

### Дней до мэтча:
```
GET: users/api/days-to-match/
```

Response (status 200):
```
{
    "days_left": 1, // полных дней до
    "hours_left": 13, // полных дней до + полных часов до
    "minutes_left": 17, // полных дней до + полных часов до + полных минут до
    "next_match_at": "2025-04-29 10:00:00" // В общем виде дата-время след.мэтча
}
```