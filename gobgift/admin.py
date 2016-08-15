from django.contrib import admin
from .models import *


@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')


class ListGroupUserInline(admin.TabularInline):
    model = ListGroupUser


@admin.register(ListGroup)
class ListGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    inlines = [
        ListGroupUserInline,
    ]
