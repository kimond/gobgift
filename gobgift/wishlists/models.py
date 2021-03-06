from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from gobgift.groups.models import ListGroup


class Wishlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.name


