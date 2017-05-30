from ..models import Gift


class TestGift:
    def test_string_representation(self):
        gift = Gift(name="Super gift")
        assert str(gift) == gift.name
