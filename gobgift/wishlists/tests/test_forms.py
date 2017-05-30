import pytest
from django.contrib.auth import get_user_model
from ..forms import WishlistForm

pytestmark = pytest.mark.django_db


class TestWishlistForm:
    @pytest.fixture()
    def user(self):
        return get_user_model().objects.create_user('Tester')

    def test_valid_data(self, user):
        form = WishlistForm(user, {'name': "My List"})
        assert form.is_valid()
        wishlist = form.save()
        assert wishlist.name, "My List"
