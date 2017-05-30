from django.conf.urls import url

from .views import GiftDelete, CommentCreate, purchase_gift, cancel_purchase_gift, GiftEdit

urlpatterns = [
    url(r'^edit/(?P<pk>\d+)/$', GiftEdit.as_view(), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', GiftDelete.as_view(), name='delete'),
    url(r'^(?P<gift_pk>\d+)/comment/add/$', CommentCreate.as_view(), name='addComment'),
    url(r'^(?P<gift_pk>\d+)/purchase/$', purchase_gift, name='purchase'),
    url(r'^(?P<gift_pk>\d+)/purchase/cancel/$', cancel_purchase_gift, name='cancelPurchase'),
]
