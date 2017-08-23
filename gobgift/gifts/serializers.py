from rest_framework import serializers

from gobgift.gifts.models import Gift, Comment


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = ('id', 'liste', 'name', 'photo', 'description',
                  'price', 'siteweb', 'store', 'purchased')

    def __init__(self, *args, **kwargs):
        exclude_purchase = kwargs.pop('exclude_purchase', None)

        super(GiftSerializer, self).__init__(*args, **kwargs)

        if exclude_purchase:
            self.fields.pop('purchased')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('gift', 'user', 'text', 'datetime')
