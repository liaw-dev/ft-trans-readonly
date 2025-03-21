"""
Django settings for pong project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
# maiman-m: decoupling to avoid modification of DATABASE values directly
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

#ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'ftpong.com', 'api.ftpong.com', '0.0.0.0']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'ftpong.com', '0.0.0.0', '*']
#config('DJANGO_ALLOWED_HOSTS')
#ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
# security theatre - double submitting
#CSRF_COOKIE_HTTPONLY = True

#SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_HOST = 'localhost'
#SECURE_SSL_HOST = 'ftpong.com'
SECURE_SSL_REDIRECT = True

# maiman-m: for allauth registration
SITE_ID = 1

# Application definition

# maiman-m: add pong apps & DRF
INSTALLED_APPS = [
    # async chat server
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # pong
    'user_profiles.apps.UserProfilesConfig',
    'friends.apps.FriendsConfig',
    'games.apps.GamesConfig',
    'frontend.apps.FrontendConfig',
    'user_auth.apps.UserAuthConfig',
    'social_auth.apps.SocialAuthConfig',
    'chat.apps.ChatConfig',
    # drf
    'rest_framework',
    'rest_framework.authtoken',
    # dj-rest-auth
    'dj_rest_auth',
    # django-allauth for standard registration
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    # geek guide
    #'sslserver',
    # drf-social-oauth2
    #'oauth2_provider',
    #'social_django',
    #'drf_social_oauth2',
    # async chat server
    #'channels',
]

# async chat server
ASGI_APPLICATION = 'pong.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        }
    }
}

# maiman-m: add django-allauth settings for mandatory email verification on sign-up and allow password reset (prevents user_logged_in signal to follow user_signed_up)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
#ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'https://ftpong.com:1100'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'https://localhost:1100'
#ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
#ACCOUNT_EMAIL_VERIFICATION = 'none'
#ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[FT_PONG] ' # 42PONG
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
#ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD
ACCOUNT_SIGNUP_REDIRECT_URL = 'https://localhost:1100'
#ACCOUNT_SIGNUP_REDIRECT_URL = 'https://ftpong.com:1100'
# register form validation
#ACCOUNT_ADAPTER = 'user_auth.adapter.CustomAccountAdapter'
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'root', 'superuser', 'django', 'pong', '42', 'test', 'user', 'default', 'avatar', 'forty-two', 'fourty-two', 'fortytwo', 'fourtytwo']
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_VALIDATORS = 'user_auth.validators.validator_list'

# drf-social-oauth2
#DRFSO2_PROPRIETARY_BACKEND_NAME = '42Intra'
#DRFSO2_URL_NAMESPACE = 'drf'
#ACTIVATE_JWT = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django-allauth for standard registration
    #'allauth.account.middleware.AccountMiddleware',
    # refresh token in body instead of header
    #'pong.middleware.MoveJWTRefreshCookieIntoTheBody',
    'pong.middleware.RequestLoggingMiddleware',
]

# maiman-m: enable drf authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # simple jwt authentication
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        # drf-social-oauth2
        #'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        #'drf_social_oauth2.authentication.SocialAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# maiman-m: add dj-rest-auth jwt support to enable jwt authentication
#CORS_ALLOW_CREDENTIALS = True
#CORS_ALLOWED_ORIGINS = ['https://ftpong.com'] # apex domain
REST_AUTH = {
    'USER_DETAILS_SERIALIZER': 'user_auth.serializers.UserLoginDetailsModelSerializer',
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    'SESSION_LOGIN': False,
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-access',
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-refresh',
    'JWT_AUTH_SECURE': True,
    # only affects the body, will still be in Set-Cookie
    #'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_SAMESITE': 'Strict',
    #'JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED': True,
}
#CSRF_TRUSTED_ORIGINS = [
#    'https://localhost',
#    'https://ftpong.com',
#]

# djangorestframework-simplejwt
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': True,
}

# django-allauth for social accounts
SOCIALACCOUNT_PROVIDERS = {
    'fortytwo': {
        'APP': {
            'client_id': config('CLIENT_ID'),
            'secret': config('CLIENT_SECRET'),
            'key': ''
        }
    }
}
SOCIALACCOUNT_ADAPTER = 'social_auth.adapter.FortyTwoSocialAccountAdapter'
FORTYTWO_URL = 'https://api.intra.42.fr/'
#SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

ROOT_URLCONF = 'pong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # maiman-m: for custom email verification template
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # maiman-m: add drf-social-oauth2 context processors
                #'social_django.context_processors.backends',
                #'social_django.context_processors.login_redirect',
            ],
        },
    },
]


WSGI_APPLICATION = 'pong.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# maiman-m: add authentication backend
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # drf-social-oauth2
    #'drf_social_oauth2.backends.DjangoOAuth2',
    # django-allauth for social accounts
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
# maiman-m: add frontend static files
STATICFILES_DIRS = [BASE_DIR / 'static'] # dev
# django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.
STATIC_ROOT = BASE_DIR / 'staticfiles' # prod

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# maiman-m: add SMTP config for email verification
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# https://docs.python.org/3/library/logging.html#logrecord-attributes
# https://docs.djangoproject.com/en/5.1/topics/logging/#configuring-logging
# https://docs.djangoproject.com/en/2.0/topics/logging/#django-request
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'formatters': {
#        'json': {
#            'format': '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}',
#        },
#        'simple': {
#            'format': '%(levelname)s %(message)s',
#        },
#    },
#    'filters': {
#        'require_debug_true': {
#            '()': 'django.utils.log.RequireDebugTrue',
#        },
#    },
#    'handlers': {
#        'console': {
#            'level': 'INFO',
#            'filters': ['require_debug_true'],
#            'class': 'logging.StreamHandler',
#            'formatter': 'simple'
#        },
#        #'logstash': {
#        #    'level': 'INFO',
#        #    'class': 'logstash.TCPLogstashHandler',
#        #    'host': 'localhost',
#        #    'port': 5000,
#        #    'version': 1,
#        #    'message_type': 'logstash',
#        #    'fqdn': False,
#        #    'tags': ['django.request'], 
#        #},
#        'file': {
#            'level': 'INFO',
#            'class': 'logging.FileHandler',
#            'filename': '/tmp/trans.log',
#            'formatter': 'json',
#        },
#    },
#    'loggers': {
#        'django.request': {
#            #'handlers': ['console', 'logstash', 'file'],
#            'handlers': ['console', 'file'],
#            'level': 'INFO',
#            'propagate': False,
#        },
#        'django.server': {
#            #'handlers': ['console', 'logstash', 'file'],
#            'handlers': ['console', 'file'],
#            'level': 'INFO',
#            'propagate': False,
#        },
#    }
#}
