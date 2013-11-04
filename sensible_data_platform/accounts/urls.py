from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^login/$', 'accounts.views.do_login', name = 'login'),
    url(r'^logout/$', 'accounts.session.logout', name = 'logout'),
    url(r'^register/$', 'accounts.register.register', name = 'register'),
    url(r'^check_username/$', 'accounts.register.check_username'),

    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
)
