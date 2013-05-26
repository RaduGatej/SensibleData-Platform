from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^openid/', include('openid_provider.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
)
