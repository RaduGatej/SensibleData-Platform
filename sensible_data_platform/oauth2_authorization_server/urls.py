from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
 #   url(r'^account/', include('oauth2_authorization_server.account_urls')),
 #   url(r'^client/', include('oauth2_authorization_server.client_urls')),
    url(r'^oauth2/', include('oauth2_authorization_server.oauth2_urls')),
 #   url(r'^', 'oauth2_authorization_server.views.home'),
)
