from django.conf.urls import url

from gobgift.gifts.views import GiftCreate
from .views import MyLists, ListCreate, view_list, ListEdit, ListDelete

urlpatterns = [
    url(r'^mylists/$', MyLists.as_view(), name='mylists'),
    url(r'^add/$', ListCreate.as_view(), name='add'),
    url(r'^view/(?P<pk>\d+)/$', view_list, name='view'),
    url(r'^edit/(?P<pk>\d+)/$', ListEdit.as_view(), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', ListDelete.as_view(), name='delete'),
    url(r'^(?P<liste_pk>\d+)/gift/add/$', GiftCreate.as_view(), name='addGift'),
]
