from django.db.models import Q
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from gobgift_api.serializers import (ListeSerializer, GiftSerializer,
                                     ListGroupSerializer, CommentSerializer,
                                     ListGroupUserSerializer)

from django.contrib.auth.models import User
from gobgift.models import Liste, Gift, ListGroup, ListGroupUser, Comment


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
        queryset = ListGroup.objects.filter(Q(users__user=user)|Q(owner=user)).distinct()
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
        my_lists = Liste.objects.all()

        serializer = self.get_serializer(my_lists, many=True)
        return Response(serializer.data)


class GiftViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing gift instances.
    """
    serializer_class = GiftSerializer
    queryset = Gift.objects.none()


class ListGiftList(generics.ListAPIView):
    """
    List gifts of a list
    """
    serializer_class = GiftSerializer
    queryset = Gift.objects.all()

    def list(self, request, pk=None):
        queryset = Liste.objects.get(id=pk).gift_set.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing comment instances.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.none()
