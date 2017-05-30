from django.contrib.auth import get_user_model
from django.test import TestCase

from gobgift.gifts.forms import GiftForm
from gobgift.wishlists.models import Wishlist


class GiftFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('Tester')
        self.wishlist = Wishlist.objects.create(name="test", owner=self.user)

    def test_init(self):
        GiftForm(wishlist=self.wishlist)

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
