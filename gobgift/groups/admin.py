from django.contrib import admin

from .models import ListGroupUser, ListGroup


class ListGroupUserInline(admin.TabularInline):
    model = ListGroupUser

@admin.register(ListGroup)
class ListGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    inlines = [
        ListGroupUserInline,
    ]
