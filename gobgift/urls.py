from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import ListeCreate, GiftCreate, GiftEdit, GiftDelete, CommentCreate

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
    url(r'^listes/$', 'gobgift.views.listes', name='listes'),
    url(r'^listes/add/$', ListeCreate.as_view(), name='addListe'),
    url(r'^listes/view/(?P<pk>\d+)/$', 'gobgift.views.viewliste', name='viewListe'),
    url(r'^listes/edit/(?P<pk>\d+)/$', 'gobgift.views.editListe', name='editListe'),
    url(r'^listes/(?P<liste_pk>\d+)/gift/add/$', GiftCreate.as_view(), name='addGift'),
    url(r'^gift/edit/(?P<pk>\d+)/$', GiftEdit.as_view(), name='editGift'),
    url(r'^gift/delete/(?P<pk>\d+)/$', GiftDelete.as_view(), name='deleteGift'),
    url(r'^gift/(?P<gift_pk>\d+)/comment/add/$', CommentCreate.as_view(), name='addComment'),
)

if settings.DEBUG :
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
