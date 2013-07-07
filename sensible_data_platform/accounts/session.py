from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from oauth2app.models import Client, AccessRange

def logout(request):
    	next = request.REQUEST.get('next', '')
	
	if request.user.is_authenticated:
		auth.logout(request)
    
	if next == '':
		return render_to_response('logout.html', {}, RequestContext(request))
	return redirect(next)
