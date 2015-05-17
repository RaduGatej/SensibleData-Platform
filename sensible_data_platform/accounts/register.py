from binascii import hexlify
import uuid
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
import simplecrypt
from utils import SECURE_platform_config

from openid_provider.models import *
from .models import *

from collections import defaultdict
import hashlib

import bson.json_util as json
from django.core.urlresolvers import reverse

from django.conf import settings
from django.contrib.auth import authenticate, login
import pdb

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


def check_cpr(request):
	status = None
	description = None
	if request.method == "GET":
		#TODO: encode and hexlify for checking
		cpr = request.GET.get("cpr")
		try:
			Participant.objects.get(cpr__exact=cpr) # TODO: sanitize input server-side
			status = -1
			description = "CPR already taken"
		except Participant.DoesNotExist:
			status = 0
			description = "CPR available for selection"
		except Exception as e:
			pdb.set_trace()
			status = -2
			description = "Something funky with the cpr"

		return HttpResponse(json.dumps([status, description])) # If here everything ok
	return HttpResponse(json.dumps("Request method not allowed")) # Should NOT reach this point

def informed_consent(request):
	informed_consent = "this is the informed consent"
	params = {}
	params['informed_consent'] = informed_consent
	return render_to_response('informed_consent.html', params, context_instance=RequestContext(request))


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
		username = request.POST.get('username', '')
		password = request.POST.get('pass1', '')
		next = request.POST.get('next', '')




		user = User.objects.create_user(username, '', password)
		user.email = request.POST.get("username", "")
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
		participant.cpr = request.POST.get('cpr', '')#simplecrypt.encrypt(SECURE_platform_config.CPR_ENCRYPTION_KEY, request.POST.get('cpr', ''))
		try: participant.pseudonym = str(hashlib.sha1(user.username.encode('utf-8')).hexdigest())[:30]
		except: participant.pseudonym = str(hashlib.sha1(user.username).hexdigest())[:30]

		participant.save()

		extra = Extra()
		extra.user = user
		extra.phone = ""
		extra.save()
		
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active: login(request, user)

		for i in range(0,10):
			child_name = request.POST.get('child_' + str(i) + '_name')
			child_cpr = request.POST.get('child_' + str(i) + '_cpr')#simplecrypt.encrypt(SECURE_platform_config.CPR_ENCRYPTION_KEY, request.POST.get('child_' + str(i) + '_cpr'))
			child_email = request.POST.get('child_' + str(i) + '_email_input')
			if child_name is None or child_cpr is None:
				break

			child_questionnaire_id = str(hashlib.sha1(child_cpr+str(uuid.uuid4())).hexdigest())
			child = Child(user=user, name=child_name, cpr=child_cpr, questionnaire_id = child_questionnaire_id, email = child_email)
			child.save()
		#return redirect(reverse('login')+'?next='+next)
		return redirect(next)



