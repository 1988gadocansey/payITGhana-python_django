"""
Django settings for payiTGhana project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DJANGO_MODE = os.getenv('DJANGO_MODE', "local").lower()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '61jpx#yv7#k=7q61@c3@vx4kwig7+92aa#^(c^jx0^emf_#6v0'

# SECURITY WARNING: don't run with debug turned on in production!
if DJANGO_MODE == 'local':
    DEBUG = True
else:
    DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = ('127.0.0.1','::1', '0.0.0.0')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'gunicorn',
    "account",
    'django_user_agents',
    'payiTGhana_App',
    'django.contrib.sites',
    #'session_security'


]
if DJANGO_MODE == 'local':
    INSTALLED_APPS += (
        'debug_toolbar',
    )




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
    "account.middleware.ExpiredPasswordMiddleware",
    'django_user_agents.middleware.UserAgentMiddleware',
    #'session_security.middleware.SessionSecurityMiddleware',

]
SITE_ID = 1
ROOT_URLCONF = 'payiTGhana-Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'payiTGhana_App', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "account.context_processors.account",
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'payiTGhana-Project.wsgi.application'
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'
MEDIA_ROOT = '/avatars'
MEDIA_URL='/media/'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'payItGhana',
			'USER': 'postgres',
			'PASSWORD': 'PRINT45dull',
			'HOST': '127.0.0.1',
			'PORT': '5432',
		}
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/app/dashboard'
LOGOUT_REDIRECT_URL = '/auth'
STATIC_ROOT = '/staticfiles'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'payiTGhana_App', 'static'),
)
TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)

# EMAIL_HOST = 'smtp.sendgrid.net',
# EMAIL_HOST_USER = os.getenv('SENDGRID_USERNAME')
# EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_PASSWORD')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE': 10
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
AVATAR_PROVIDERS=[
    'avatar.providers.PrimaryAvatarProvider',
    'avatar.providers.GravatarAvatarProvider',
    'avatar.providers.DefaultAvatarProvider',
]
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_PASSWORD_EXPIRY = 60*60*24*5  # seconds until pw expires, this example shows five days
ACCOUNT_PASSWORD_USE_HISTORY = True
LOGIN_URL = '/auth/'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'gadocansey@gmail.com'
EMAIL_HOST_PASSWORD = '1988gadocansey'
EMAIL_PORT = 587