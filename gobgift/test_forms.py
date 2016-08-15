from django.contrib.auth import get_user_model
from django.test import TestCase

from .forms import GiftForm, ListeForm
from .models import Liste


class ListeFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('Tester')

    def test_init(self):
        ListeForm(self.user)

    def test_valid_data(self):
        form = ListeForm(self.user, {'name': "My List"})
        self.assertTrue(form.is_valid())
        wishlist = form.save()
        self.assertEquals(wishlist.name, "My List")


class GiftFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('Tester')
        self.wishlist = Liste.objects.create(name="test", owner=self.user)

    def test_init(self):
        GiftForm(liste=self.wishlist)

    def test_valid_data(self):
        form = GiftForm(self.wishlist, {
            'name': 'supergift',
            'photo': None,
            'description': 'Gift to test',
            'price': None,
            'store': None,
            'siteweb': None
        })
        self.assertTrue(form.is_valid())
        gift = form.save()
        self.assertEquals(gift.name, "supergift")
