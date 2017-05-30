from .base import *

# django-debug-toolbar
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar',)

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

ALLOWED_HOSTS = ['0.0.0.0', 'localhost']
