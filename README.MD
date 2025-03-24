
## Описание API

### 1. Регистрация пользователя

#### Чтобы зарегистрировать пользователя, необходимо выполнить следующий POST-запрос:

```json 
/users/api/register/
```

#### Параметры запроса:
```json
{
  "username": "имя_пользователя",
  "email": "почта@example.com",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "age": 25,
  "university": "Университет",
  "image": "ссылка_на_изображение",
  "password": "пароль"
}
```

#### Условия:
* Пароли password1 и password2 из формы должны совпадать, необходимо проверить на frontend.
* В хедере запроса необходимо передавать токен администратора:
```json
  Authorization: token <admin_token>
```

##### Для получения <admin_token> необходимо сделать POST-запрос c полями username и password для суперпользователя.
```json 
auth/token/login/
```

#### Ответ:
```json
{
    "user": {
        "id": 12,
        "username": "имя_пользователя",
        "email": "почта@example.com",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "age": 25,
        "university": "Университет",
        "image": "ссылка_на_изображение"
    },
    "token": "86a2afcc646af04e2617019c2",
    "uniq_code": "f6de81a7-a99c-6514d57fab10"
}
```

#### Примечание:
* token и uniq_code - генерируются на backend автоматически

#### После успешной регистрации фронтенд должен:
* Сохранить полученный token.
* Сформировать ссылку на Telegram-бота в следующем формате:
```json
https://t.me/Uni_Match_Bot?start=uniq_code
```


### 2. Авторизация пользователя (два способа)
#### 1) Авторизация через форму (логин/email + пароль)
```json
POST /auth/token/login/
```

#### Параметры запроса
```json
{
  "username": "логин_или_email",
  "password": "пароль"
}
```

#### В хедере запроса необходимо передавать токен администратора:
```json
  Authorization: token <admin_token>
```

#### Ответ:
```json
{
  "auth_token": "токен_пользователя_для_авторизации"
}
```

Полученный токен необходимо сохранить в сессиях браузера для дальнейших запросов.

#### 2) Авторизация через Telegram-бота
#### Для этого необходимо:
##### 1. Сделать GET-запрос:
```json
GET запрос на /users/api/generate-uniq-code/
```
##### 2. Ответ будет содержать уникальный код:
```json
{
  "uniq_code": "уникальный_код"
}
```
##### 3. Сформировать ссылку на Telegram-бота в формате:
```json
https://t.me/Uni_Match_Bot?start=login_<uniq_code>
```

##### 4. Пользователь переходит по этой ссылке, и в боте происходит связывание uniq_code с chat_id.
##### 5. После этого нужно выполнить GET запрос на:
```json
/users/api/get-user-by-uniq-code/<uniq_code>/
```
##### 6. Ответ будет содержать данные пользователя и его токен:
```json
{
    "user": {
        "id": 12,
        "username": "имя_пользователя",
        "email": "почта@example.com",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "age": 25,
        "university": "Университет",
        "image": "ссылка_на_изображение"
    },
    "token": "86a2afc4e2617019c2"
}
```

##### 7. Необходимо сохранить token в сессиях браузера.

## Запуск Django-проекта на локальной машине

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
