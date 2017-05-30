from django.contrib.auth import get_user_model
from django.test import TestCase

from ..forms import WishlistForm


class WishlistFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('Tester')

    def test_init(self):
        WishlistForm(self.user)

    def test_valid_data(self):
        form = WishlistForm(self.user, {'name': "My List"})
        self.assertTrue(form.is_valid())
        wishlist = form.save()
        self.assertEquals(wishlist.name, "My List")
