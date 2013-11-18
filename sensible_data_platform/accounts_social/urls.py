from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^login/$', 'accounts_social.views.login', name = 'login'),
    url(r'^register/$', 'accounts_social.views.login', name = 'register'),

    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
)
