from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
import datetime


class ListGroup(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def get_view_url(self):
        return reverse('viewGroup', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('editGroup', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('deleteGroup', kwargs={'pk': self.id})

    def get_adduser_url(self):
        return reverse('addGroupUser', kwargs={'listgroup_pk': self.id})

    def is_user_admin(self, user):
        """
        Valide if the user has admin rights
        """
        listGroupUser = self.users.filter(user=user)
        if len(listGroupUser) > 0:
            return listGroupUser[0].is_admin
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


class Liste(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    groups = models.ManyToManyField(ListGroup, related_name='lists')

    def get_view_url(self):
        return reverse('viewList', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('editList', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('deleteList', kwargs={'pk': self.id})

    def get_addgift_url(self):
        return reverse('addGift', kwargs={'liste_pk': self.id})

    def __unicode__(self):
        return self.name


class Gift(models.Model):
    liste = models.ForeignKey(Liste)
    name = models.CharField(max_length=150, verbose_name=_('Name'))
    photo = models.ImageField(upload_to='gifts', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    price = models.FloatField(null=True, blank=True, verbose_name=_('Price'))
    siteweb = models.CharField(null=True, blank=True, max_length=350)
    store = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Store'))
    purchased = models.BooleanField(default=False)

    def get_edit_url(self):
        return reverse('editGift', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('deleteGift', kwargs={'pk': self.id})

    def get_addcomment_url(self):
        return reverse('addComment', kwargs={'gift_pk': self.id})

    def get_purchased_url(self):
        return reverse('purchasedGift', kwargs={'gift_pk': self.id})

    def get_cancelpurchased_url(self):
        return reverse('cancelPurchasedGift', kwargs={'gift_pk': self.id})

    def __unicode__(self):
        return self.name


class Purchase(models.Model):
    gift = models.ForeignKey(Gift, related_name="purchase")
    user = models.ForeignKey(User)


class Comment(models.Model):
    gift = models.ForeignKey(Gift)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=300)
    datetime = models.DateTimeField(auto_now_add=True, default=datetime.datetime.today)


