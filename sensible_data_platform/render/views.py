from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required


def home(request):
	return render_to_response('index.html', {})

@login_required
def profile(request):
	values = {}
	values['user'] = manager.getUser(request.user)
	values['connector_link'] = {}
	values['connector_link']['cas'] = platform_config.IDENTITY_PROVIDERS['CAS']['link']
	return render_to_response('profile.html', values)
