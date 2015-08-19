from django.contrib import admin
from .models import *

@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
    pass


class ListGroupUserInline(admin.TabularInline):
    model = ListGroupUser


@admin.register(ListGroup)
class ListGroupAdmin(admin.ModelAdmin):
    inlines = [
       ListGroupUserInline,
    ]
