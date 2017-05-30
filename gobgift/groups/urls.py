from django.conf.urls import url

from .views import MyGroups, GroupCreate, view_group, GroupEdit, GroupDelete, ListGroupUserCreate, GroupUserDelete

urlpatterns = [
    url(r'^mygroups/$', MyGroups.as_view(), name='mygroups'),
    url(r'^add/$', GroupCreate.as_view(), name='add'),
    url(r'^view/(?P<pk>\d+)/$', view_group, name='view'),
    url(r'^edit/(?P<pk>\d+)/$', GroupEdit.as_view(), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', GroupDelete.as_view(), name='delete'),
    url(r'^(?P<listgroup_pk>\d+)/user/add/$', ListGroupUserCreate.as_view(), name='addUser'),
    url(r'^deleteuser/(?P<pk>\d+)/$', GroupUserDelete.as_view(), name='deleteUser'),
]
