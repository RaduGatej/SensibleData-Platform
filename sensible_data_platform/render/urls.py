from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^profile/', 'render.profile.profile', name='profile'),
    url(r'^dashboard/?$', 'render.dashboard.dashboard', name='dashboard'),
    url(r'^authorizations/?$', 'render.authorizations.authorizations', name='authorizations'),
    url(r'^applications/?$', 'render.applications.applications', name='applications'),
    url(r'^home/?$', 'render.views.home', name='home'),
    url(r'^about/?$', 'render.about.about', name='about'),
    url(r'^', 'render.views.home'),
)
