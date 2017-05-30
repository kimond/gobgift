from ..models import Wishlist


class WishlistTest:
    def test_string_representation(self):
        wish_list = Wishlist(name="Test list")
        assert str(wish_list) == wish_list.name
