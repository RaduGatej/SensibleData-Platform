from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import urllib2
from oauth2app.models import Client, AccessRange, ClientType, AccessToken

def logout(request):
	next = request.REQUEST.get('next', '')
	
	if request.user.is_authenticated:
		try:
			user = request.user
			for client in Client.objects.filter(type=ClientType.objects.get(type='study')):
				urllib2.urlopen(client.api_uri+'logout/?access_token=%s'%AccessToken.objects.filter(user=user, scope=AccessRange.objects.get(key='enroll'), client=client)[0].token)
		except: pass


		auth.logout(request)

    
	if next == '':
		return render_to_response('logout.html', {}, RequestContext(request))
	return redirect(next)
