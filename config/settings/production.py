from .base import *

import environ

env = environ.Env()

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['gobgift.kimond.com', ])

ADMIN_URL = env('DJANGO_ADMIN_URL')

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

SENTRY_DSN = env('DJANGO_SENTRY_DSN')
SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')