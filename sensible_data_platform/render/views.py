from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from service_manager import service_manager

def home(request):
	if not request.user.is_authenticated():
		return render_to_response('index.html', {}, context_instance=RequestContext(request))


	services = service_manager.getServices2(request.user)

	#TODO this simple logic support only one authorization url per application, we need auth per scope 
	for service in services:
		if 'error' in services[service]: continue
		for application in services[service]['applications']:
			for scope in services[service]['applications'][application]['scopes']:
				services[service]['applications'][application]['auth_url'] = services[service]['applications'][application]['scopes'][scope]['auth_url']
				services[service]['applications'][application]['authorized'] = services[service]['applications'][application]['scopes'][scope]['authorized']


	#return HttpResponse(json.dumps(services))
	return render_to_response('home_studies.html', {'services': services}, context_instance=RequestContext(request))
