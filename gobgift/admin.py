from django.contrib import admin
from .models import *

@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
    pass


@admin.register(ListGroup)
class ListGroupAdmin(admin.ModelAdmin):
    pass
