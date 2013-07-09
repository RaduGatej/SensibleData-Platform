from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^profile/', 'render.profile.profile', name='profile'),
    url(r'^dashboard/?$', 'render.dashboard.dashboard', name='dashboard'),
    url(r'^authorizations/?$', 'render.authorizations.authorizations', name='authorizations'),
    url(r'^home/?$', 'render.views.home', name='home'),
    url(r'^', 'render.views.home'),
)
