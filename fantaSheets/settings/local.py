from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
# stored in environment variable
SECRET_KEY = 'CHANGE ME!'

ALLOWED_HOSTS = []


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fantasheetsdb',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    }
}
