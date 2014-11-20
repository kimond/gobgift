from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
import datetime


class Liste(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=150)

    def get_view_url(self):
        return reverse('viewListe', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('editListe', kwargs={'pk': self.id})

    def get_addgift_url(self):
        return reverse('addGift', kwargs={'liste_pk': self.id})

    def __unicode__(self):
        return self.name


class Gift(models.Model):
    liste = models.ForeignKey(Liste)
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='gifts', null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    siteweb = models.CharField(null=True, blank=True, max_length=350)
    store = models.CharField(null=True, blank=True, max_length=150)

    def get_edit_url(self):
        return reverse('editGift', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('deleteGift', kwargs={'pk': self.id})

    def get_addcomment_url(self):
        return reverse('addComment', kwargs={'gift_pk': self.id})

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    gift = models.ForeignKey(Gift)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=300)
    datetime = models.DateTimeField(auto_now_add=True, default=datetime.datetime.today)


