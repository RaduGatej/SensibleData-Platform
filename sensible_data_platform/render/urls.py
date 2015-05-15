from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^i18n/', include('django.conf.urls.i18n')),
	url(r'^changebrowser','render.views.changebrowser',name='changebrowser'),
	url(r'^noscript','render.views.noscript', name='noscript'),
	url(r'^profile/?$', 'render.profile.profile', name='profile'),
	url(r'^login_child/?$', 'render.views.login_child', name='login_child'),
	url(r'^notify_child/?$', 'render.views.notify_child', name='notify_child'),
    url(r'^dashboard/?$', 'render.dashboard.dashboard', name='dashboard'),
    url(r'^authorizations/?$', 'render.authorizations.authorizations', name='authorizations'),
    url(r'^applications/?$', 'render.applications.applications', name='applications'),
    url(r'^home/?$', 'render.views.home', name='home'),
    url(r'^about/?$', 'render.about.about', name='about'),
    url(r'^', 'render.views.home'),
)
