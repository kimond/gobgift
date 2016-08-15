from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import response
from rest_framework import schemas
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.decorators import detail_route, list_route, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from gobgift_api.serializers import (ListeSerializer, GiftSerializer,
                                     ListGroupSerializer, CommentSerializer,
                                     ListGroupUserSerializer)

from django.contrib.auth.models import User
from gobgift.models import Liste, Gift, ListGroup, ListGroupUser, Comment


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Gobgift API')
    return response.Response(generator.get_schema(request=request))


class ListGroupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing listgroup instances
    """
    serializer_class = ListGroupSerializer
    queryset = ListGroup.objects.none()

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
    serializer_class = ListeSerializer
    queryset = Liste.objects.all()

    def list(self, request, pk=None):
        queryset = ListGroup.objects.get(id=pk).lists.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListGroupUserViewSet(viewsets.ModelViewSet):
    serializer_class = ListGroupUserSerializer
    queryset = ListGroupUser.objects.none()


class ListeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing list instances.
    """
    serializer_class = ListeSerializer
    queryset = Liste.objects.none()

    def list(self, request):
        """
        List the user's lists
        """
        user = User.objects.get(pk=request.user.pk)
        my_lists = Liste.objects.filter(owner=user)
        serializer = self.get_serializer(my_lists, many=True)
        return Response(serializer.data)


class GiftViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    A viewset for viewing and editing gift instances.
    """
    serializer_class = GiftSerializer
    queryset = Gift.objects.all()

    def retrieve(self, request, pk=None):
        queryset = Gift.objects.all()
        gift = get_object_or_404(queryset, pk=pk)
        serializer = GiftSerializer(gift)
        if gift.liste.owner == request.user:
            serializer = GiftSerializer(gift, exclude_purchase=True)

        return Response(serializer.data)


class ListGiftList(generics.ListAPIView):
    """
    List gifts of a list
    """
    serializer_class = GiftSerializer
    queryset = Gift.objects.all()

    def list(self, request, pk=None):
        list_queryset = Liste.objects.all()
        wishlist = get_object_or_404(list_queryset, pk=pk)
        queryset = Liste.objects.get(id=pk).gift_set.all()
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
