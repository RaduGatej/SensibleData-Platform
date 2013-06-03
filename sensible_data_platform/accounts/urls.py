from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'accounts.session.logout'),
    (r'^register/$', 'accounts.register.register'),
)
