from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "abcdef")

DEBUG = os.getenv("DEBUG", True)

# !!!!! change or delete
TELEGRAM_BOT_TOKEN = "7852631020:AAGv3e97G8_OoJKlrKx2m97LM3iLwgI6c5c"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    "corsheaders",
    # OAuth
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if os.getenv("DOCKER_PROJECT"):
    DATABASES = {
        'default': {
            "ENGINE": "django.db.backends.postgresql",
            'HOST': os.getenv("DB_HOST"),
            'NAME': os.getenv("DB_NAME"),
            'USER': os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASS"),
            'PORT': '5432'
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = [
    "djangoProject.auth_backends.EmailAuthBackend",
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
    'social_core.backends.telegram.TelegramAuth',
]

# 1692072411
# 1692072411

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Yekaterinburg'
USE_TZ = True

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if os.getenv("DOCKER_PROJECT"):
    MEDIA_ROOT = '/vol/web/media'
    STATIC_ROOT = '/vol/web/static'
else:
    MEDIA_ROOT = BASE_DIR / 'media_dev'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',

        # 'oauth2_provider.contrib.rest_framework.0Auth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
}

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserSerializer',
    }
}


CORS_ALLOW_ALL_ORIGINS = True  # поменять!
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "https://2160-95-164-87-45.ngrok-free.app"
]

# https://2160-95-164-87-45.ngrok-free.app/users/tg-btn-auth/


SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

DJOSER = {
    'SERIALIZERS': {
        'user': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
        'token': 'users.serializers.CustomTokenSerializer',
    },
    'LOGIN_FIELD': 'email',
}