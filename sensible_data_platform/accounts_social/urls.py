from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^accounts/authenticate/?$', 'accounts_social.views.authenticate', name = 'authenticate'),
    url(r'^accounts/login/?$', 'accounts_social.views.authenticate', name = 'login'),
    url(r'^accounts/register/?$', 'accounts_social.views.authenticate', name = 'register'),

    url(r'^profile/?$', 'accounts_social.views.profile', name='profile'),

    url(r'^accounts/social/', include('social.apps.django_app.urls', namespace='social')),
)
