from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from gobgift.groups.models import ListGroup


class Wishlist(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    groups = models.ManyToManyField(ListGroup, related_name='lists', blank=True)

    def get_view_url(self):
        return reverse('lists:view', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('lists:edit', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('lists:delete', kwargs={'pk': self.id})

    def get_addgift_url(self):
        return reverse('lists:addGift', kwargs={'liste_pk': self.id})

    def __unicode__(self):
        return self.name


