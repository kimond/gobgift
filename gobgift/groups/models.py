from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class ListGroup(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User)

    def __unicode__(self):
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
        list_group_user = self.users.filter(user=user)
        if len(list_group_user) > 0:
            return list_group_user[0].is_admin
        else:
            return False


class ListGroupUser(models.Model):
    group = models.ForeignKey(ListGroup, related_name="users")
    user = models.ForeignKey(User, related_name="listgroups")
    is_admin = models.BooleanField(default=False)

    def get_delete_url(self):
        return reverse('deleteGroupUser', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name
