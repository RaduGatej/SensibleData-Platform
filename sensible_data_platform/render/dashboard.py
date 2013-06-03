from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required
from service_manager import service_manager


@login_required
def dashboard(request):
	template = {}
	template['services'] = service_manager.getServices(request.user)
	template['authorizations'] = service_manager.getAuthorizations(request.user, template['services'])
	return HttpResponse(json.dumps(template))
	return render_to_response('dashboard.html', template)
