#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.context_processors import csrf
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
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
		session_key = request.session.session_key
		children = []
		for child in children_objects:
			child_questionnaire_url = settings.BASE_URL + "login_child" + "?parent_session=" + session_key + "&type_id=" "child_" + child.questionnaire_id
			parent_questionnaire_url = settings.BASE_URL + "login_child" + "?parent_session=" + session_key + "&type_id=" + "parent_" + child.questionnaire_id
			child_dict = model_to_dict(child)
			child_dict["child_questionnaire_url"] = child_questionnaire_url
			child_dict["parent_questionnaire_url"] = parent_questionnaire_url
			children.append(child_dict)
		return render_to_response("child_list.html", {"children":children}, context_instance=RequestContext(request))

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
	parent_session_key = request.GET.get("parent_session")
	type_id = request.GET.get("type_id")
	parent_session = Session.objects.get(session_key=parent_session_key)
	uid = parent_session.get_decoded().get('_auth_user_id')

	user = User.objects.get(pk=uid)

	user.backend = 'django.contrib.auth.backends.ModelBackend'

	login(request, user)

	return HttpResponseRedirect(settings.QUESTIONNAIRE_APP_URL + "?type_id=" + type_id)


def notify_child(request):
	if request.method == 'POST':
		message =  unicode(u"Velkommen til Youth Gaming Project!\n\n")
		message += unicode(u"Din forælder har tilmeldt dig forskningsprojektet Youth Gaming Project (YGP). Følg venligst dette link for at starte spørgeskemaet: " ) 
		message += unicode(request.POST["child_questionnaire_link"])
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


