from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views import defaults as default_views

from gobgift.api.views import FacebookLogin, GoogleLogin
from gobgift.core.views import home, logout, done, app, privacy_policy
from gobgift.groups.views import ListGroupAutocomplete
from gobgift.groups.views import UserAutocomplete

urlpatterns = [
    path('', home, name="home"),
    path('app/', app, name="app"),
    path('login/', home),
    path('logout/', logout),
    path('done/', done, name='done'),
    path('privacy/', privacy_policy, name='privacy'),
    path(settings.ADMIN_URL, admin.site.urls),
    path(r'accounts', include('allauth.urls')),

    path(r'lists/', include(('gobgift.wishlists.urls', 'gobgift.wishlists'), namespace='lists')),
    path(r'gifts/', include(('gobgift.gifts.urls', 'gobgift.gifts'), namespace='gifts')),
    path(r'groups/', include(('gobgift.groups.urls', 'gobgift.groups'), namespace='groups')),

    # DjangoRestFramework
    path(r'api/', include(('gobgift.api.urls', 'gobgift.api'), namespace='api')),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'rest-auth/', include('rest_auth.urls')),
    path(r'rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path(r'rest-auth/google/', GoogleLogin.as_view(), name='rest_google_login'),

    # Django autocomplete light
    path(r'user-autocomplete/', UserAutocomplete.as_view(), name="user-autocomplete"),
    path(r'listgroup-autocomplete/', ListGroupAutocomplete.as_view(), name="listgroup-autocomplete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('403/', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path('500/', default_views.server_error),
        path('__debug__/', include(debug_toolbar.urls)),
        # url(r'^docs/$', serve, {'document_root': settings.DOCS_ROOT, 'path': 'index.html'}),
        # url(r'^docs/(?P<path>.*)$', serve, {'document_root': settings.DOCS_ROOT}),
    ]
