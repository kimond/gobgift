from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from gobgift.api.views import schema_view, FacebookLogin, GoogleLogin
from gobgift.core.views import home, logout, done, app
from gobgift.groups.views import ListGroupAutocomplete
from gobgift.groups.views import UserAutocomplete

urlpatterns = [

    url(r'^$', home, name="home"),
    url(r'^app/$', app, name="app"),
    url(r'^login/$', home),
    url(r'^logout/$', logout),
    url(r'^done/$', done, name='done'),
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'accounts', include('allauth.urls')),

    url(r'^lists/', include('gobgift.wishlists.urls', namespace='lists')),
    url(r'^gifts/', include('gobgift.gifts.urls', namespace='gifts')),
    url(r'^groups/', include('gobgift.groups.urls', namespace='groups')),

    # DjangoRestFramework
    url(r'^api/', include('gobgift.api.urls', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),
    url(r'^docs/', schema_view),

    # Django autocomplete light
    url(r'^user-autocomplete/$', UserAutocomplete.as_view(),
        name="user-autocomplete"),
    url(r'^listgroup-autocomplete/$', ListGroupAutocomplete.as_view(),
        name="listgroup-autocomplete"),
]

if settings.DEBUG:
    import debug_toolbar

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
                       url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
                       url(r'^403/$', default_views.permission_denied,
                           kwargs={'exception': Exception('Permission Denied')}),
                       url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
                       url(r'^500/$', default_views.server_error),
                       url(r'^__debug__/', include(debug_toolbar.urls)),
                       # url(r'^docs/$', serve, {'document_root': settings.DOCS_ROOT, 'path': 'index.html'}),
                       # url(r'^docs/(?P<path>.*)$', serve, {'document_root': settings.DOCS_ROOT}),
                   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
