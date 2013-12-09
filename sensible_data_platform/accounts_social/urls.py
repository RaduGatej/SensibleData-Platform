from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^authenticate/$', 'accounts_social.views.authenticate', name = 'authenticate'),
    url(r'^login/$', 'accounts_social.views.authenticate', name = 'login'),
    url(r'^register/$', 'accounts_social.views.authenticate', name = 'register'),

    url(r'^profile/$', 'accounts_social.views.profile', name = 'profile'),

    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
)
