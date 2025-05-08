## API документация

### Регистрация

```
  POST api/register/
```

```http 
{
  "email": "почта@example.com",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "birth": "2000-01-28",
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
        "birth": "2000-01-28",
        "chat_id": null,
        "image": null,
        "hobby": [
            {
                "id": 1,
                "name": "Программирование"
            },
            {
                "id": 2,
                "name": "Спорт"
            }],
    },
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```

Сохранить access токен на клиенте.

Response (status 400):

```
{
    "error": "Пользователь с таким email уже существует."
}
```

На клиенте проверить валидность email, first_name, last_name, birth на формат.
Пароли проверить на равенство.

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
    "access": "<access_token>"
  }
```

Необходимо сохранить access токен на клиенте.

Ошибка 400:

```http
{
    "error": "Неверный email или пароль"
}
```

### Обновление access-токен

Условие, при котором необходимо обновить access-токен:
если получен ответ с кодом 401 (при доступе к контенту и т.д)/

```
POST: api/token/refresh/
```

Response (status 200):

```http
{
    "access": "<access_token>",
}
```

Если ошибка 401, то редирект на страницу с авторизацией.

### Получение текущего пользователя по JWT-токену

```
GET: api/auth/users/me/
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
    "birth": "2000-08-12",
    "chat_id": null,
    "image": null,
    "hobby": [
        {
            "id": 1,
            "name": "Программирование"
        },
        {
            "id": 2,
            "name": "Спорт"
        }
    ]
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
POST: api/tg-auth/
```

Пример использования:
[Пример](https://github.com/ordenmeny/UniMatch-django-backend/blob/main/users/templates/users/tg_auth.html)

Код успешного ответа: 201.

### Получение истории мэтчей текущего пользователя:

```
GET: api/pairs/
```

```
Authorization: Bearer <access_token>
```

Response (status 200):

```
{
    "current_pair": {
        "id": 228,
        "partner": {
            "id": 45,
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "email@example.com",
            "hobby": [
                {
                    "id": 1,
                    "name": "Программирование"
                },
                {
                    "id": 2,
                    "name": "Спорт"
                },
                {
                    "id": 5,
                    "name": "Рисование"
                }
            ]
        },
        "created_at": "2025-05-08"
    },
    "pairs": [
        {
            "id": 225,
            "partner": {
                "id": 31,
                "first_name": "Дмитрий",
                "last_name": "Александров",
                "email": "admin@yandex.ru",
                "hobby": [
                    {
                        "id": 1,
                        "name": "Программирование"
                    },
                    {
                        "id": 2,
                        "name": "Спорт"
                    },
                    {
                        "id": 7,
                        "name": "История"
                    }
                ]
            },
            "created_at": "2025-05-08"
        },
        {
            "id": 226,
            "partner": {
                "id": 58,
                "first_name": "Дэн",
                "last_name": "Рейнолдс",
                "email": "danraynolds15@example.com",
                "hobby": [
                    {
                        "id": 1,
                        "name": "Программирование"
                    },
                    {
                        "id": 2,
                        "name": "Спорт"
                    },
                    {
                        "id": 5,
                        "name": "Рисование"
                    }
                ]
            },
            "created_at": "2025-05-08"
        }
    ]
}
```

### Получение списка тэгов

```
GET: api/hobby/all/
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
GET: api/hobby/total/
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

### Дней до мэтча:

```
GET: api/days-to-match/
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

### Обновление данных пользователя (в т.ч хобби)

```
PATCH api/update/user/
```

```
Authorization: Bearer <access_token> 
```

Передаем только те данные, которые были изменены.

```
{
  "first_name": "Дэн",
  "last_name": "Рейнолдс",
  "birth": "2000-01-28",
  "hobby": [1, 2, 7],
  "tg_link": "@user-dan"
}
```

Response (status 200):

```
{
    "id": 59,
    "first_name": "Дэн",
    "last_name": "Рейнолдс",
    "email": "danraynolds16@example.com",
    "birth": "2000-01-28",
    "chat_id": null,
    "image": null,
    "hobby": [
        1,
        2,
        7
    ],
    "tg_link": "@user-dan"
}
```

### Запуск Django-проекта на локальной машине

#### 1. Клонируйте репозиторий:
```bash
git clone <url_репозитория>
cd <папка_проекта>
```

#### 2. Создайте и активируйте виртуальное окружение:
###### Для Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
###### Для Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```
#### 3. Установите зависимости:
```bash
pip install -r req.txt
```

#### 4. Настройте базу данных:
```bash
python manage.py makemigrations
python manage.py migrate
``` 

#### 5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

#### 6. Запустите сервер:
```bash
python manage.py runserver
```
##### Сервер будет доступен по адресу http://127.0.0.1:8000