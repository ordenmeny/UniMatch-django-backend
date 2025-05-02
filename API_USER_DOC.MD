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