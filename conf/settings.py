import os
from pathlib import Path
# import environ
import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()
# Initialize environ
# env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
# Read environment variables from .env file
# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
# Build paths inside the project like this: BASE_DIR / 'subdir'.



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^fkv0x+kc+++d3gm2o4u-6l3au9_*-jjhv&+(3$6q^&8gmt-5)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'basic_app',
    'django_celery_beat',
    # 'rangefilter',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'face_data',
        'USER': 'postgres',
        'PASSWORD': '998359015a@',
        'HOST': '95.130.227.29',  
        'PORT': '5432',
    }
}


WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# settings.py
TIME_ZONE = 'Asia/Tashkent'
USE_TZ = True


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
# MEDIA_URL = 'http://face-admin.misterdev.uz/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Statik va Media URL

STATICFILES_DIRS = []
# Statik va Media Fayllar Katalogi
# STATIC_ROOT = '/var/www/workers/face_data/static/'
# MEDIA_ROOT = '/var/www/workers/face_data/media/'

# Collectstatic natijasida yaratilgan fayllar manifestini boshqarish uchun
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'



CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',  # yoki Memcached
        'LOCATION': 'redis://127.0.0.1:6379/1',      # Redis misol
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
    "face-id.misterdev.uz"
]

ID_2488986=os.getenv("ID_2488986")
ID_2488993=os.getenv("ID_2488993")
ID_2488999=os.getenv("ID_2488999")
ID_2489002=os.getenv("ID_2489002")
ID_2489005=os.getenv("ID_2489005")
ID_2489007=os.getenv("ID_2489007")
ID_2489012=os.getenv("ID_2489012")
ID_2489019=os.getenv("ID_2489019")
username=os.getenv("username")
password=os.getenv("password")


face_ids = {
    "ID_2488986": os.getenv("ID_2488986"),
    "ID_2488993": os.getenv("ID_2488993"),
    "ID_2488999": os.getenv("ID_2488999"),
    "ID_2489002": os.getenv("ID_2489002"),
    "ID_2489005": os.getenv("ID_2489005"),
    "ID_2489007": os.getenv("ID_2489007"),
    "ID_2489012": os.getenv("ID_2489012"),
    "ID_2489019": os.getenv("ID_2489019"),
}

# None bo'lganlarni chiqarib tashlash
face_ids = {key: value for key, value in face_ids.items() if value is not None}
# print(
#     'from seetings', face_ids
# )
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis broker URL
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CONN_MAX_AGE = 60