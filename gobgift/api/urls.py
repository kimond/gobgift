from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from gobgift.api.views import (WishlistViewSet, GiftViewSet, ListGroupViewSet,
                               CommentViewSet, ListGroupUserViewSet,
                               ListGiftList, ListGroupList, GiftCommentList, current_user)

schema_view = get_swagger_view(title='Gobgift API')

router = routers.DefaultRouter()
router.register(r'lists', WishlistViewSet, base_name='wishlist')
router.register(r'gifts', GiftViewSet)
router.register(r'listgroups', ListGroupViewSet, base_name='group')
router.register(r'listgroupusers', ListGroupUserViewSet)
router.register(r'comments', CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'', include(router.urls)),
    url(r'current_user/$', current_user),
    url(r'^lists/(?P<pk>\d+)/gifts', ListGiftList.as_view(),
        name='list-gift-list'),
    url(r'^listgroups/(?P<pk>\d+)/lists', ListGroupList.as_view(),
        name='listgroup-list-list'),
    url(r'^gifts/(?P<pk>\d+)/comments', GiftCommentList.as_view(),
        name='gift-comment-list'),
    url(r'docs/$', schema_view)
]
