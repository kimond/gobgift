from django.test import TestCase

from ..models import Gift


class GiftTest(TestCase):
    def test_string_representation(self):
        gift = Gift(name="Super gift")
        self.assertEquals(str(gift), gift.name)
