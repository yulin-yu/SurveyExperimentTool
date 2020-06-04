import os
import sys
import environ
import logging
from boto3.session import Session

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

SITE_ID = env('SITE_ID', default=1)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
# DEBUG = True  # that's temporary just for debug on server

ALLOWED_HOSTS = ['*']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG,
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'crispy_forms',
    'workflow',
    'django.contrib.admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'workflow.middlewares.WorkerIdAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'workflow.auth_backends.WorkerIdBackend',

]

if 'test' not in sys.argv:
    MIDDLEWARE = [
                     'debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

ROOT_URLCONF = 'core.urls'
TEMPLATE_LOADERS = ['django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates")
        ],
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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'core.wsgi.application'

RDS = env('RDS', default=False)
if RDS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'sqlite3',
            #'USER': env('RDS_USERNAME'),
            #'PASSWORD': env('RDS_PASSWORD'),
            #'HOST': env('RDS_HOSTNAME'),
            #'PORT': env('RDS_PORT'),
        }
    }
else:
    DATABASES = {
        'default': env.db(),
    }

# CELERY_BROKER_URL = env('CELERY_BROKER_URL')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# if DEBUG and env('USE_EMAIL_IN_DEBUG') == 'False':
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# elif not DEBUG or env('USE_EMAIL_IN_DEBUG') == 'True':
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_HOST = env('EMAIL_HOST')
#     EMAIL_USE_TLS = env('EMAIL_USE_TLS')
#     EMAIL_PORT = env('EMAIL_PORT')
#     EMAIL_HOST_USER = env('EMAIL_HOST_USER')
#     EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
VERSION = os.getenv('VERSION', 'mrf.18.10.2019.3')

MTURK_ENDPOINT = env(
    'MTURK_ENDPOINT',
    default='https://mturk-requester-sandbox.us-east-1.amazonaws.com')
MTURK_WORKER_ENDPOINT = env('MTURK_WORKER_ENDPOINT',
                            default='https://workersandbox.mturk.com')

MTURK_REGION = env('MTURK_REGION')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None

INTERNAL_IPS = (
    '127.0.0.1',
)

LOGIN_URL = '/admin/login/'

### aws xray configuration

INSTALLED_APPS += [
    'django_aws_xray'
]

boto3_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name='us-east-2')



MIDDLEWARE.insert(0, 'django_aws_xray.middleware.XRayMiddleware')

# Enable various instrumentation monkeypatches
AWS_XRAY_PATCHES = [
    'django_aws_xray.patches.cache',
    'django_aws_xray.patches.redis',
    'django_aws_xray.patches.db',
    'django_aws_xray.patches.requests',
    'django_aws_xray.patches.templates',
]
