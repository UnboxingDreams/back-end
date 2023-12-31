"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from firebase_admin import initialize_app, credentials
from google.auth import load_credentials_from_file
from google.oauth2.service_account import Credentials
import os
import redis
from environ import Env


# Build paths inside the project like this: BASE_DIßR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


env = Env(DEBUG=False)
env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

SECRET_KEY = env('SECRET_KEY')
JWT_ALGO = env("JWT_ALGO")
REDIS_ENDPOINT = os.environ.get("REDIS_ENDPOINT")
REDIRECT_URI = env("REDIRECT_URI")
REST_SECRET_KEY = env("REST_SECRET_KEY")
REST_API_KEY = env("REST_API_KEY")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_NAME = env("AWS_STORAGE_NAME")
FRONT_URL = env("FRONT_URL")
GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET")
APPLE_CLIENT_ID = env("APPLE_CLIENT_ID")
APPLE_KEY_ID = env("APPLE_KEY_ID")
APPLE_ISS = env("APPLE_ISS")
APPLE_SITE = env("APPLE_SITE")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

APPEND_SLASH = False

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'petmourning',
    'app',
    'app.otherurls',
    'django_apscheduler',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    #'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    "petmourning.views.authorization.JsonWebTokenMiddleWare",

]
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
CORS_ALLOW_HEADERS = ["*"]
#CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

#CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = ['http://localhost:3000', 'http://127.0.0.1:3000']

ROOT_URLCONF = 'app.urls'

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




# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : env("DB_NAME"),
        'USER' : env("DB_USER"),
        'PASSWORD' : env("DB_PASS"),
        'HOST' : env("DB_HOST"),
        'PORT' : '3306',
    }
}

REDIS_ENDPOINT = "redis://127.0.0.1:6379"

REDIS = redis.StrictRedis.from_url(REDIS_ENDPOINT)

CACHES = {
	"default": {
    	"BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION" : "redis://redis_service:6379/1",
        "OPTIONS": {
        	"CLIENT_CLASS" : "django_redis.client.DefaultClient",
        }
    }
}



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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WSGI_APPLICATION = 'app.wsgi.application'


# For FCM

cred = credentials.Certificate("petmourningFCM.json")
FIREBASE_APP = initialize_app(cred)


FCM_DJANGO_SETTINGS = {
     # an instance of firebase_admin.App to be used as default for all fcm-django requests
     # default: None (the default Firebase app)
    "DEFAULT_FIREBASE_APP": FIREBASE_APP,
     # default: _('FCM Django')
    "APP_VERBOSE_NAME": "[string for AppConfig's verbose_name]",
     # true if you want to have only one active device per registered user at a time
     # default: False
    "ONE_DEVICE_PER_USER": True,
     # devices to which notifications cannot be sent,
     # are deleted upon receiving error response from FCM
     # default: False
    "DELETE_INACTIVE_DEVICES": False,
}



APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default

SCHEDULER_DEFAULT = True

