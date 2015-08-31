# coding=utf-8
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
from documents.get_documents import getText

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
		encrypted_cpr = request.GET.get("cpr")
		#encrypted_cpr = simplecrypt.encrypt(SECURE_platform_config.CPR_ENCRYPTION_KEY, cpr).encode("hex")
		try:
			CPRNumber.objects.get(cpr__exact=encrypted_cpr) # TODO: sanitize input server-side
			status = -1
			description = "CPR already taken"
		except CPRNumber.DoesNotExist:
			status = 0
			description = "CPR available for selection"
		except Exception as e:
			status = -2
			description = "Something funky with the cpr"

		return HttpResponse(json.dumps([status, description])) # If here everything ok
	return HttpResponse(json.dumps("Request method not allowed")) # Should NOT reach this point

def check_child_email(request):

	if request.method == "GET":
		#TODO: encode and hexlify for checking
		child_email = request.GET.get("child_email")
		#child_email = simplecrypt.encrypt(SECURE_platform_config.CPR_ENCRYPTION_KEY, cpr).encode("hex")
		try:
			Child.objects.get(email__exact=child_email) # TODO: sanitize input server-side
			status = -1
			description = "Email already taken"
		except Child.DoesNotExist:
			status = 0
			description = "Email available for selection"
		except Exception as e:
			status = -2
			description = "Something funky with the Email"

		return HttpResponse(json.dumps([status, description])) # If here everything ok
	return HttpResponse(json.dumps("Request method not allowed")) # Should NOT reach this point


def informed_consent(request, text, title, next, accept="Acceptér", reject="Nej tak"):
	informed_consent = text
	params = {}
	params['next'] = next
	params['informed_consent'] = informed_consent
	params['title'] = title
	params['accept'] = accept
	params['reject'] = reject
	return render_to_response('informed_consent.html', params, context_instance=RequestContext(request))


def informed_consent_stub(request):
	informed_consent_text = getText("informed_consent", "da")
	params = {'informed_consent': informed_consent_text}
	return render_to_response('informed_consent_stub.html', params, context_instance=RequestContext(request))


def parent_intro(request):
	text = getText("parent_intro", "da")
	return informed_consent(request, text, 'Information om projektet', 'parent_informed_consent', reject="Jeg ønsker ikke at deltage", accept="Deltag")


def parent_informed_consent(request):
	text = getText("informed_consent", "da")
	return informed_consent(request, text, 'Samtykkeerklæring', 'register')


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
		parent_cpr = request.POST.get('cpr', '')
		encrypted_cpr = CPRNumber(cpr=parent_cpr)#simplecrypt.encrypt(SECURE_platform_config.CPR_ENCRYPTION_KEY, parent_cpr).encode("hex"))
		encrypted_cpr.save()
		participant.cpr = encrypted_cpr
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
			child_cpr = request.POST.get('child_' + str(i) + '_cpr')
			if child_name is None or child_cpr is None:
				break
			encrypted_cpr = CPRNumber(cpr=child_cpr)#simplecrypt.encrypt(SECURE_platform_config.CPR_ENCRYPTION_KEY, child_cpr).encode("hex"))
			encrypted_cpr.save()
			child_email = request.POST.get('child_' + str(i) + '_email_input')
			child_questionnaire_id = str(hashlib.sha1(encrypted_cpr.cpr[:10]+str(uuid.uuid4())).hexdigest())
			child = Child(user=user, name=child_name, cpr=encrypted_cpr, questionnaire_id = child_questionnaire_id, email = child_email)
			child.save()
		#return redirect(reverse('login')+'?next='+next)
		return redirect(next)


def register_child(request):
	if request.method == "POST":
		user = User.objects.get(username=request.user.username)
		if not user:
			if user.is_active:
				login(request, user)

		child_name = request.POST.get('child_name')
		child_cpr = request.POST.get('child_cpr')
		if child_name is None or child_cpr is None:
			return redirect("/platform/home/")
		encrypted_cpr = CPRNumber(cpr=child_cpr)#simplecrypt.encrypt(SECURE_platform_config.CPR_ENCRYPTION_KEY, child_cpr).encode("hex"))
		encrypted_cpr.save()
		child_email = request.POST.get('child_email_input')
		child_questionnaire_id = str(hashlib.sha1(encrypted_cpr.cpr[:10]+str(uuid.uuid4())).hexdigest())
		child = Child(user=user, name=child_name, cpr=encrypted_cpr, questionnaire_id = child_questionnaire_id, email = child_email)
		child.save()

	return redirect("/platform/home/")

