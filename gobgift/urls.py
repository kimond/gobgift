from django.conf.urls import include, url
from django.contrib import admin

from .views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'gobgift.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name="home"),
    url(r'^login/$', home),
    url(r'^logout/$', logout),
    url(r'^done/$', done, name='done'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^email/$', require_email, name='require_email'),
    url('', include('social.apps.django_app.urls', namespace='social')),

    # List urls
    url(r'^mylists/$', mylists, name='mylists'),
    url(r'^lists/add/$', ListCreate.as_view(), name='addList'),
    url(r'^lists/view/(?P<pk>\d+)/$', view_list, name='viewList'),
    url(r'^lists/edit/(?P<pk>\d+)/$', ListEdit.as_view(), name='editList'),
    url(r'^lists/delete/(?P<pk>\d+)/$', ListDelete.as_view(), name='deleteList'),
    url(r'^lists/(?P<liste_pk>\d+)/gift/add/$', GiftCreate.as_view(), name='addGift'),

    # Gift urls
    url(r'^gift/edit/(?P<pk>\d+)/$', GiftEdit.as_view(), name='editGift'),
    url(r'^gift/delete/(?P<pk>\d+)/$', GiftDelete.as_view(), name='deleteGift'),
    url(r'^gift/(?P<gift_pk>\d+)/comment/add/$', CommentCreate.as_view(), name='addComment'),
    url(r'^gift/(?P<gift_pk>\d+)/purchased/$', purchased_gift, name='purchasedGift'),
    url(r'^gift/(?P<gift_pk>\d+)/purchased/cancel/$', cancel_purchased_gift, name='cancelPurchasedGift'),

    # Group urls
    url(r'^mygroups/$', mygroups, name='mygroups'),
    url(r'^group/add/$', GroupCreate.as_view(), name='addGroup'),
    url(r'^group/view/(?P<pk>\d+)/$', view_group, name='viewGroup'),
    url(r'^group/edit/(?P<pk>\d+)/$', GroupEdit.as_view(), name='editGroup'),
    url(r'^group/delete/(?P<pk>\d+)/$', GroupDelete.as_view(), name='deleteGroup'),
    url(r'^group/(?P<listgroup_pk>\d+)/user/add/$', ListGroupUserCreate.as_view(), name='addGroupUser'),
    url(r'^groupuser/delete/(?P<pk>\d+)/$', GroupUserDelete.as_view(), name='deleteGroupUser'),

    # DjangoRestFramework
    url(r'^api/', include('gobgift_api.urls', namespace='gobgift_api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-oauth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api-oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # Django autocomplete light
    url(r'^user-autocomplete/$', UserAutocomplete.as_view(),
        name="user-autocomplete"),
    url(r'^listgroup-autocomplete/$', ListGroupAutocomplete.as_view(),
        name="listgroup-autocomplete"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ]
