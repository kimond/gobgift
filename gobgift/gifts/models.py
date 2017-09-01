from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

from gobgift.wishlists.models import Wishlist


class Gift(models.Model):
    wishlist = models.ForeignKey(Wishlist)
    name = models.CharField(max_length=150, verbose_name=_('Name'))
    photo = models.ImageField(upload_to='gifts', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    price = models.FloatField(null=True, blank=True, verbose_name=_('Price'))
    website = models.CharField(null=True, blank=True, max_length=350)
    store = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Store'))
    purchased = models.BooleanField(default=False)

    def get_edit_url(self):
        return reverse('gifts:edit', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('gifts:delete', kwargs={'pk': self.id})

    def get_addcomment_url(self):
        return reverse('gifts:addComment', kwargs={'gift_pk': self.id})

    def get_purchased_url(self):
        return reverse('gifts:purchase', kwargs={'gift_pk': self.id})

    def get_cancelpurchased_url(self):
        return reverse('gifts:cancelPurchase', kwargs={'gift_pk': self.id})

    def __str__(self):
        return self.name


class Purchase(models.Model):
    gift = models.ForeignKey(Gift, related_name="purchase")
    user = models.ForeignKey(User)


class Comment(models.Model):
    gift = models.ForeignKey(Gift)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=300)
    datetime = models.DateTimeField(auto_now_add=True)
