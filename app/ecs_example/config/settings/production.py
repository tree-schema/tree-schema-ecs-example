
import json
import os

from .base import *

# These will be injected by ECS from our AWS Secrets Manager!
DJANGO_ECS_SECRETS = json.loads(env("DJANGO_ECS_SECRETS"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_ECS_SECRETS['DJANGO_SECRET_KEY']

# This should be changed to your host once it is updated
# https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['yourdomain.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DJANGO_ECS_SECRETS['POSTGRES_DB'],
        'USER': DJANGO_ECS_SECRETS['POSTGRES_USER'],
        'PASSWORD': DJANGO_ECS_SECRETS['POSTGRES_PASSWORD'],
        'HOST': DJANGO_ECS_SECRETS['POSTGRES_HOST'],
        'PORT': DJANGO_ECS_SECRETS['POSTGRES_PORT']
     }
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

# Celery
# ------------------------------------------------------------------------------
_redis_host = os.environ['REDIS_HOST']
CELERY_BROKER_URL = f'redis://{_redis_host}:6379/0'
CELERY_TASK_DEFAULT_QUEUE = 'ecs_example'

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = env('AWS_REGION')
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'


# AWS_REGION_NAME = env("AWS_REGION")


# Serve Content from CloudFront
# ------------------------------------------------------------------------------
INSTALLED_APPS = ["collectfast", "storages"] + INSTALLED_APPS

# Variables used by django-storages & collectfast
STATICFILES_STORAGE = "config.settings.production.StaticRootS3Boto3Storage"
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
AWS_S3_CUSTOM_DOMAIN = env("MY_STATIC_CDN")
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

# Required since storages doesn't pick up on Role access
AWS_ACCESS_KEY_ID = DJANGO_ECS_SECRETS['DJANGO_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = DJANGO_ECS_SECRETS['DJANGO_AWS_SECRET_ACCESS_KEY']


# This defines the specific location and access for the objects in the bucket
# It is not required but can give fine-grained control and can be used if 
# you want to have different storage locations (buckets) used by this package
from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402

class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
