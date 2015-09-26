#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core import signing
from django.core.context_processors import csrf
from django.core.signing import SignatureExpired, BadSignature
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
import json

from accounts import manager
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from accounts.models import Child
from oauth2app.models import Client
from password_reset.utils import send_email
from render.forms import ChildNotificationForm
from service_manager import service_manager
from collections import defaultdict
from sensible_platform_documents.get_documents import getText
from utils import SECURE_platform_config


def home(request):
	if not request.user.is_authenticated():
		text = {}
		text['welcome'] = getText('welcome_text', request.LANGUAGE_CODE)
		return render_to_response('index.html', {'text': text}, context_instance=RequestContext(request))

	#return HttpResponseRedirect(settings.QUESTIONNAIRE_APP_URL)

	status = request.REQUEST.get('status', '')
	message = request.REQUEST.get('message', '')

	services = service_manager.getServices2(request.user,request.LANGUAGE_CODE)
	render_services = dict()


	#return HttpResponse(json.dumps(services))
	service = services[services.keys()[0]]

	if 'error' in service:
		return HttpResponseRedirect(service["authorize_url"])
	else:
		#return HttpResponseRedirect(settings.QUESTIONNAIRE_APP_URL)
		children_objects = Child.objects.filter(user=User.objects.get(username=request.user.username))
		children = []
		for child in children_objects:
			parent_questionnaire_url = settings.QUESTIONNAIRE_APP_URL + "?" + urllib.urlencode({"type_id": "parent_" + child.questionnaire_id})
			child_dict = model_to_dict(child, exclude=['questionnaire_id', 'user', 'cpr', 'relation_to_user'])
			child_dict["id"] = int(child_dict["id"])
			child_dict["parent_questionnaire_url"] = parent_questionnaire_url
			children.append(child_dict)
		return render_to_response("child_list.html", {"children": children}, context_instance=RequestContext(request))

	for service in services:
		render_services[service] = {}
		if 'error' in services[service]:
			return HttpResponseRedirect(services[service]["authorize_url"])
			render_services[service] = services[service] #not authorized
			continue
		render_services[service]['description'] = services[service]['discovery']
		render_services[service]['applications'] = {}
		for application in services[service]['applications']:
			render_services[service]['applications'][application] = {}
			render_services[service]['applications'][application]['description'] = services[service]['applications'][application]['description']
			render_services[service]['applications'][application]['uri'] = services[service]['applications'][application]['uri']


			render_services[service]['applications'][application]['scopes'] = {}
			for scope in services[service]['applications'][application]['scopes']:
				try:
					render_services[service]['applications'][application]['scopes'][services[service]['applications'][application]['scopes'][scope]['auth_url']['url']][scope] = services[service]['applications'][application]['scopes'][scope]

				except KeyError:
					render_services[service]['applications'][application]['scopes'][services[service]['applications'][application]['scopes'][scope]['auth_url']['url']] = {}
					render_services[service]['applications'][application]['scopes'][services[service]['applications'][application]['scopes'][scope]['auth_url']['url']][scope] = services[service]['applications'][application]['scopes'][scope]

				render_services[service]['applications'][application]['scopes'][services[service]['applications'][application]['scopes'][scope]['auth_url']['url']]['message'] = services[service]['applications'][application]['scopes'][scope]['auth_url']['message']

				try:
					render_services[service]['applications'][application]['scopes'][services[service]['applications'][application]['scopes'][scope]['auth_url']['url']]['status'] *= int(services[service]['applications'][application]['scopes'][scope]['authorized'])
				except KeyError:
					render_services[service]['applications'][application]['scopes'][services[service]['applications'][application]['scopes'][scope]['auth_url']['url']]['status'] = 1
					render_services[service]['applications'][application]['scopes'][services[service]['applications'][application]['scopes'][scope]['auth_url']['url']]['status'] *= int(services[service]['applications'][application]['scopes'][scope]['authorized'])


	text = {}
	
	text['projects_header'] = getText('projects_header', request.LANGUAGE_CODE)

	return render_to_response('home_studies.html', {'services': dict(render_services), 'status': status, 'message': message, 'text': text}, context_instance=RequestContext(request))


def changebrowser(request):
	return render_to_response('changebrowser.html', {}, context_instance=RequestContext(request))

def noscript(request):
	return render_to_response('js_disabled.html', {}, context_instance=RequestContext(request))

def see_informed_consent(request):
	service_name = request.GET.get("service_name")
	client = Client.objects.get(name=service_name)
	return render_to_response('informed_consent.html', {'informed_consent': service_manager.getInformedConsent(client,request.LANGUAGE_CODE)}, context_instance=RequestContext(request))


def login_child(request):
	login_token = request.GET.get("token")
	uid = -1
	try:
		uid = signing.loads(login_token, salt=SECURE_platform_config.CHILD_LINK_SALT, max_age=settings.CHILD_LINK_AGE)
	except SignatureExpired, e:
		return render_to_response('expired_token.html', context_instance=RequestContext(request))
	except BadSignature, e:
		return Http404

	type_id = request.GET.get("type_id")

	user = User.objects.get(pk=uid)
	user.backend = 'django.contrib.auth.backends.ModelBackend'

	login(request, user)

	return HttpResponseRedirect(settings.QUESTIONNAIRE_APP_URL + "?type_id=" + type_id)


def notify_child(request):
	if request.method == 'POST':
		child_id = int(request.POST["child_id"])
		child = Child.objects.get(pk=child_id)

		uid = User.objects.get(username=request.user.username).pk
		token = signing.dumps(uid, salt=SECURE_platform_config.CHILD_LINK_SALT)

		child_questionnaire_url = settings.BASE_URL + "login_child" + "?" + urllib.urlencode({"token": token, "type_id": "child_" + child.questionnaire_id})

		message = unicode(u"Velkommen til Youth Gaming Project!\n\n")
		message += unicode(u"Din forælder har tilmeldt dig forskningsprojektet Youth Gaming Project (YGP). Følg venligst dette link for at starte spørgeskemaet: " ) 
		message += unicode(child_questionnaire_url)
		message += unicode(u"\n\n")
		message += unicode(u"Opbevar denne mail i tilfælde af, at du holder pause undervejs og vil komme tilbage til spørgeskemaet senere. Hvis du mister linket, kan du altid bede din forælder om at sende dig et nyt link.")
		message += unicode(u"\n\nMed venlig hilsen\nYouth Gaming Project")

		send_email(request.POST["child_email"], message, subject="Youth Gaming Project spørgeskema")

		try:
			children = Child.objects.filter(email=request.POST["child_email"])
			for child in children:
				child.notified = True
				child.save()
		except:
			return HttpResponseRedirect('/home/')

		return HttpResponseRedirect('/home/')

	return HttpResponseRedirect('/home/')


