from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext

from openid_provider.models import *
from .models import *

from collections import defaultdict
import hashlib

import bson.json_util as json
from django.core.urlresolvers import reverse

from django.conf import settings
from django.contrib.auth import authenticate, login

def check_username(request):
	username = None
	status = None
	description = None
	if request.method == "GET":
		username = request.GET.get("username")
		if len(username) < 6 :
			status = -1
			description = "Username must be at lest 6 characters"
		else :
			try:
				user = User.objects.get(username__exact=username) # TODO: sanitize input server-side
				status = -2
				description = "Username already taken"
			except User.DoesNotExist:
				user = None
				status = 0
				description = "Username available for selection"
			except:
				status = -2
				description = "Something funky with the username"

		return HttpResponse(json.dumps([status, description])) # If here everything ok
	return HttpResponse(json.dumps("Request method not allowed")) # Should NOT reach this point

def register(request):

	if request.method == 'GET':
		values = defaultdict(dict)
		values['next'] = request.REQUEST.get('next', '')
		if values['next'] == '': values['next'] = reverse('home')
		values.update(csrf(request))
		values['platformUri'] = settings.BASE_URL
		values['next'] += '&registration=true'
		return render_to_response('registration/register.html', values, context_instance=RequestContext(request))

	if request.method == 'POST':

		next = request.POST.get('next', '')

		_register(request.POST.get('username', ''), request.POST.get('pass1', ''))

		user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('pass1', ''))
		if user is not None:
			if user.is_active: login(request, user)

		#return redirect(reverse('login')+'?next='+next)
		return redirect(next)


def _register(username, password = ''):
	user = User.objects.create_user(username, '', password)
	user.email = username
	user.save()

	openid = OpenID()
	openid.user = user
	openid.default = True
	openid.save()

	for trust_root in settings.TRUST_ROOTS:
		try: TrustedRoot.objects.create(openid=openid, trust_root=trust_root)
		except: pass


	participant = Participant()
	participant.user = user
	try: participant.pseudonym = str(hashlib.sha1(user.username.encode('utf-8')).hexdigest())[:30]
	except: participant.pseudonym = str(hashlib.sha1(user.username).hexdigest())[:30]
	participant.save()

	extra = Extra()
	extra.user = user
	extra.phone = ""
	extra.save()

	return user
