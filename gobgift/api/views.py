from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_auth.registration.views import SocialLoginView
from rest_framework import response
from rest_framework import schemas
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.decorators import detail_route, list_route, api_view, renderer_classes
from rest_framework.response import Response

from gobgift.gifts.models import Gift, Comment
from gobgift.gifts.serializers import GiftSerializer, CommentSerializer
from gobgift.groups.models import ListGroup, ListGroupUser
from gobgift.groups.serializers import ListGroupSerializer, ListGroupUserSerializer
from gobgift.wishlists.models import Wishlist

from django.contrib.auth.models import User

from gobgift.wishlists.serializers import WishlistSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class ListGroupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing listgroup instances
    """
    serializer_class = ListGroupSerializer

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.pk)
        return ListGroup.objects.filter(Q(users__user=user) | Q(owner=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):
        """
        List the user's listgroups
        """
        user = User.objects.get(pk=request.user.pk)
        queryset = ListGroup.objects.filter(Q(users__user=user) | Q(owner=user)).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListGroupList(generics.ListAPIView):
    """
    List the lists of a listgroup
    """
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()

    def list(self, request, pk=None):
        queryset = ListGroup.objects.get(id=pk).lists.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListGroupUserViewSet(viewsets.ModelViewSet):
    serializer_class = ListGroupUserSerializer
    queryset = ListGroupUser.objects.none()


class WishlistViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing wishlist instances.
    """
    serializer_class = WishlistSerializer

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.pk)
        return Wishlist.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):
        """
        List the user's lists
        """
        user = User.objects.get(pk=request.user.pk)
        my_lists = Wishlist.objects.filter(owner=user)
        serializer = self.get_serializer(my_lists, many=True)
        return Response(serializer.data)


class GiftViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing gift instances.
    """
    serializer_class = GiftSerializer
    queryset = Gift.objects.all()

    def retrieve(self, request, pk=None):
        queryset = Gift.objects.all()
        gift = get_object_or_404(queryset, pk=pk)
        serializer = GiftSerializer(gift)
        if gift.wishlist.owner == request.user:
            serializer = GiftSerializer(gift, exclude_purchase=True)

        return Response(serializer.data)


class ListGiftList(generics.ListAPIView):
    """
    List gifts of a list
    """
    serializer_class = GiftSerializer
    queryset = Gift.objects.all()

    def list(self, request, pk=None):
        list_queryset = Wishlist.objects.all()
        wishlist = get_object_or_404(list_queryset, pk=pk)
        queryset = Wishlist.objects.get(id=pk).gift_set.all()
        serializer = self.get_serializer(queryset, many=True)
        if wishlist.owner == request.user:
            serializer = self.get_serializer(queryset, many=True, exclude_purchase=True)
        return Response(serializer.data)


class GiftCommentList(generics.ListAPIView):
    """
    List comments on a gift
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def list(self, request, pk=None):
        gift_queryset = Gift.objects.all()
        gift = get_object_or_404(gift_queryset, pk=pk)
        queryset = Gift.objects.get(pk=pk).comment_set.all()
        serializer = self.get_serializer(queryset, many=True)
        if gift.liste.owner == request.user:
            raise PermissionDenied("Owner of this gift can't see the comments")
        return Response(serializer.data)


class CommentViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
    A viewset for viewing and editing comment instances.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
