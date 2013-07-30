from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from service_manager import service_manager
from collections import defaultdict

def home(request):
	if not request.user.is_authenticated():
		return render_to_response('index.html', {}, context_instance=RequestContext(request))


	services = service_manager.getServices2(request.user)
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
	



	#return HttpResponse(json.dumps(render_services))
	return render_to_response('home_studies.html', {'services': dict(render_services)}, context_instance=RequestContext(request))
