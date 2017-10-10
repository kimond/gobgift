import environ

env = environ.Env()

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['gobgift.kimond.com', ])

ADMIN_URL = env('DJANGO_ADMIN_URL')
