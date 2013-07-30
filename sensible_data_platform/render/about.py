from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required
from service_manager import service_manager
from django.template import RequestContext


def about(request):
		return render_to_response('about.html', {}, context_instance=RequestContext(request))
