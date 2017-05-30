from ..models import Gift


class GiftTest:
    def test_string_representation(self):
        gift = Gift(name="Super gift")
        assert str(gift) == gift.name
