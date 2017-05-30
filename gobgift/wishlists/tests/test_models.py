from django.test import TestCase

from ..models import Wishlist


class WishlistTest(TestCase):
    def test_string_representation(self):
        wish_list = Wishlist(name="Test list")
        self.assertEquals(str(wish_list), wish_list.name)
