from django.test import TestCase

from gobgift.models import ListGroup, Liste, Gift


class ListGroupTest(TestCase):
    def test_string_representation(self):
        list_group = ListGroup(name="Test")
        self.assertEquals(str(list_group), list_group.name)


class ListeTest(TestCase):
    def test_string_representation(self):
        wishlist = Liste(name="Test list")
        self.assertEquals(str(wishlist), wishlist.name)


class GiftTest(TestCase):
    def test_string_representation(self):
        gift = Gift(name="Super gift")
        self.assertEquals(str(gift), gift.name)
