from rest_framework import serializers

from gobgift.core.serializers import UserSerializer
from gobgift.wishlists.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'owner', 'name', 'groups')
