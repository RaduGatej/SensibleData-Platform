from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^login/$', 'accounts.views.do_login', name = 'login'),
    url(r'^logout/$', 'accounts.session.logout', name = 'logout'),
    url(r'^register/$', 'accounts.register.register_not_allowed', name = 'register'),
	url(r'^informed_consent/$', 'accounts.register.parent_informed_consent', name = 'parent_informed_consent'),
	url(r'^parent_intro/$', 'accounts.register.parent_intro', name = 'parent_intro'),
	url(r'^informed_consent_stub/$', 'accounts.register.informed_consent_stub', name = 'informed_consent_stub'),
    url(r'^check_username/$', 'accounts.register.check_username'),
	url(r'^modify_child_email/$', 'accounts.register.can_modify_child_email'),
	url(r'^check_child_email/$', 'accounts.register.check_child_email'),
	url(r'^check_cpr/$', 'accounts.register.check_cpr'),
    url(r'^', include('password_reset.urls')),
)
