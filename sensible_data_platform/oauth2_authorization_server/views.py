from django.shortcuts import render_to_response
from django.template import RequestContext
from oauth2app.models import Client, AccessToken
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


@login_required
#@staff_member_required
def home(request):
	template = {}
	if request.user.is_authenticated():
		clients = Client.objects.filter(user=request.user)
		access_tokens = AccessToken.objects.filter(user=request.user)
		access_tokens = access_tokens.select_related()
		template["access_tokens"] = access_tokens
		template["clients"] = clients
	return render_to_response('oauth2/home.html', template, RequestContext(request))
