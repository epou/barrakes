from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zp)&o10z!@bj--+_i5&_e%q5gr7ukqbmoafgo6#a4hjdyv*rw+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}