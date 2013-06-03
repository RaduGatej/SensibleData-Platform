#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
        (r'^missing_redirect_uri/?$',   'oauth2_authorization_server.oauth2.missing_redirect_uri'),
        (r'^authorize/?$',              'oauth2_authorization_server.oauth2.authorize'),
        (r'^token/?$',                  'oauth2app.token.handler'),
)
