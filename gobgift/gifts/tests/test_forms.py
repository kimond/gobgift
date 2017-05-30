import pytest
from django.contrib.auth import get_user_model

from gobgift.gifts.forms import GiftForm
from gobgift.wishlists.models import Wishlist

pytestmark = pytest.mark.django_db


class GiftFormTest:
    @pytest.fixture()
    def user(self):
        return get_user_model().objects.create_user('Tester')

    @pytest.fixture()
    def wishlist(self, user):
        return Wishlist.objects.create(name="test", owner=user)

    def test_valid_data(self, wishlist):
        form = GiftForm(wishlist, {
            'name': 'supergift',
            'photo': None,
            'description': 'Gift to test',
            'price': None,
            'store': None,
            'siteweb': None
        })
        assert form.is_valid()
        gift = form.save()
        assert gift.name == "supergift"
