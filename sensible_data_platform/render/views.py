from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import json

from accounts import manager
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from oauth2app.models import Client
from service_manager import service_manager
from collections import defaultdict
from sensible_platform_documents.get_documents import getText

def home(request):
	if not request.user.is_authenticated():
		text = {}
		text['welcome'] = getText('welcome_text', request.LANGUAGE_CODE)
		return render_to_response('index.html', {'text': text}, context_instance=RequestContext(request))

	return HttpResponseRedirect(settings.QUESTIONNAIRE_APP_URL)

	status = request.REQUEST.get('status', '')
	message = request.REQUEST.get('message', '')

	services = service_manager.getServices2(request.user,request.LANGUAGE_CODE)
	render_services = dict()


	#return HttpResponse(json.dumps(services))

	for service in services:
		render_services[service] = {}
		if 'error' in services[service]:
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
