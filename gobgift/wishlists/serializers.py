from rest_framework import serializers

from gobgift.wishlists.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Wishlist
        fields = ('id', 'owner', 'name', 'groups')


