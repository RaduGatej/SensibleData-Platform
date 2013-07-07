from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required
from service_manager import service_manager


@login_required
def dashboard(request):
	#TODO: this should host visualizations of the data flows
	template = {}
	template['username'] = str(request.user.get_full_name())
	template['services'] = service_manager.getServices(request.user)
	#template['authorizations'] = json.dumps(service_manager.getAuthorizations(request.user, template['services']))
	#TODO: sort services by name
	template['services'] = json.dumps(template['services'])
	#return HttpResponse(json.dumps(template))
	return render_to_response('dashboard_bootstrap.html', template, context_instance=RequestContext(request))
