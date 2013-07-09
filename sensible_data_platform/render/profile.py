from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


@login_required
def profile(request):
	values = {}
	values['connector_link'] = {}
	values['connector_link']['cas'] = platform_config.IDENTITY_PROVIDERS['CAS']['link']
	return render_to_response('profile.html', values, context_instance=RequestContext(request))
