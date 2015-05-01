#-*- coding: utf-8 -*-


from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from uni_form.helpers import FormHelper, Submit, Reset
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser
from oauth2app.models import *
from .forms import AuthorizeForm
from django.core.urlresolvers import reverse
from service_manager import whitelist, service_manager
import json

@login_required
def missing_redirect_uri(request):
    return render_to_response(
        'oauth2/missing_redirect_uri.html', 
        {}, 
        RequestContext(request))


@login_required
def authorize(request):
	authorizer = Authorizer()
	try:
		authorizer.validate(request)
	except MissingRedirectURI, e:
		return HttpResponseRedirect("/oauth2/oauth2/missing_redirect_uri")
	except AuthorizationException, e:
		# The request is malformed or invalid. Automatically 
		# redirects to the provided redirect URL.
		return authorizer.error_redirect()

	if not whitelist.checkWhitelist(authorizer.user, authorizer.client):
		return authorizer.error_redirect()

	if request.method == 'GET':
		template = {
				"client":authorizer.client, 
				"access_ranges":authorizer.access_ranges}
		template["form"] = AuthorizeForm()
		helper = FormHelper()
		no_submit = Submit('connect','No', css_class='btn btn-large')
		helper.add_input(no_submit)
		yes_submit = Submit('connect', 'Godkend', css_class='btn btn-large btn-success')
		helper.add_input(yes_submit)
		helper.form_action = reverse('oauth2_authorize')+'?%s' % authorizer.query_string
		helper.form_method = 'POST'
		template["helper"] = helper

		is_enrollment = False
		try:
			is_enrollment = AccessRange.objects.get(key='enroll') in authorizer.access_ranges
		except AccessRange.DoesNotExist: pass

		if is_enrollment:
			return authorizer.grant_redirect()
			template['informed_consent'] = service_manager.getInformedConsent(authorizer.client,request.LANGUAGE_CODE)

			return render_to_response(
				'oauth2/authorize_enroll.html', 
				template, 
				RequestContext(request))
		return render_to_response(
				'oauth2/authorize.html', 
				template, 
				RequestContext(request))
	elif request.method == 'POST':
		form = AuthorizeForm(request.POST)
		if form.is_valid():
			if request.POST.get("connect") == "Godkend":
				return authorizer.grant_redirect()
			else:
				return authorizer.error_redirect()
	return HttpResponseRedirect("/")
