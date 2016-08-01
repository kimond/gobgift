from django.contrib.auth.models import User
from django.test import TestCase

from gobgift.models import ListGroup, Liste, Gift, ListGroupUser


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


class ListGroupUserTest(TestCase):
    def test_string_representation(self):
        user = User.objects.create_user(username="johnd", first_name="John", email="test@test.com", last_name="Deer")
        list_group_user = ListGroupUser(user=user)
        string_representation = user.first_name + " " + user.last_name
        self.assertEquals(str(list_group_user), string_representation)
