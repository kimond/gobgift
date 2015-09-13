from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gobgift.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'gobgift.views.home', name="home"),
    url(r'^login/$', 'gobgift.views.home'),
    url(r'^logout/$', 'gobgift.views.logout'),
    url(r'^done/$', 'gobgift.views.done', name='done'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^email/$', 'gobgift.views.require_email', name='require_email'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^mylists/$', 'gobgift.views.mylists', name='mylists'),
    url(r'^lists/add/$', ListCreate.as_view(), name='addList'),
    url(r'^lists/view/(?P<pk>\d+)/$', 'gobgift.views.viewlist', name='viewList'),
    url(r'^lists/edit/(?P<pk>\d+)/$', 'gobgift.views.editList', name='editList'),
    url(r'^lists/(?P<liste_pk>\d+)/gift/add/$', GiftCreate.as_view(), name='addGift'),
    url(r'^gift/edit/(?P<pk>\d+)/$', GiftEdit.as_view(), name='editGift'),
    url(r'^gift/delete/(?P<pk>\d+)/$', GiftDelete.as_view(), name='deleteGift'),
    url(r'^gift/(?P<gift_pk>\d+)/comment/add/$', CommentCreate.as_view(), name='addComment'),
    url(r'^mygroups/$', 'gobgift.views.mygroups', name='mygroups'),
    url(r'^group/add/$', GroupCreate.as_view(), name='addGroup'),
    url(r'^group/view/(?P<pk>\d+)/$', 'gobgift.views.viewGroup', name='viewGroup'),
)

if settings.DEBUG :
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
