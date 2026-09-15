import configparser
from pathlib import Path

from django.db.backends.mysql.base import DatabaseWrapper

#Existing project customization
#DatabaseWrapper.data_types['DateTimeField'] = 'datetime'
#Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

#Static and Template files
TEMPLATE_URL = BASE_DIR / 'templates'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

#Configuration file
config = configparser.ConfigParser()
config.read(BASE_DIR / "config.ini")

#Roles
admin_role = config.get("ROLE", "ADMIN")
user_role = config.get("ROLE", "USER")

#Security
SECRET_KEY = config.get("DJANGO", "SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = []

#Installed Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_filters',
    'base',

]
#Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#URLs
ROOT_URLCONF = 'project.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_URL],
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

#WSGI
WSGI_APPLICATION = 'project.wsgi.application'

#Database
DATABASES = {
    'default': {
        'ENGINE': config.get("DATA_BASE", "ENGINE"),
        'NAME': config.get("DATA_BASE", "NAME"),
        'USER': config.get("DATA_BASE", "USER"),
        'PASSWORD': config.get("DATA_BASE", "PASSWORD"),
        'HOST': config.get("DATA_BASE", "HOST"),
        'PORT': config.get("DATA_BASE", "PORT"),
        'OPTIONS': {
            'charset': 'utf8'
        }
    }
}
#Password Validation
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

#Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False

#Primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'