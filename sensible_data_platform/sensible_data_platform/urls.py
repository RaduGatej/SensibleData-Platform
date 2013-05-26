from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^openid/', include('openid_provider.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^identity_providers/', include('identity_providers.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('render.urls')),
)
