from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class ListGroup(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_view_url(self):
        return reverse('groups:view', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('groups:edit', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('groups:delete', kwargs={'pk': self.id})

    def get_adduser_url(self):
        return reverse('groups:addUser', kwargs={'listgroup_pk': self.id})

    def is_user_admin(self, user):
        """
        Valide if the user has admin rights
        """
        try:
            group_user = self.users.get(user=user)
            return group_user.is_admin
        except ListGroupUser.DoesNotExist:
            return False


class ListGroupUser(models.Model):
    group = models.ForeignKey(ListGroup, related_name="users", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="listgroups", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def get_delete_url(self):
        return reverse('groups:deleteUser', kwargs={'pk': self.id})

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
