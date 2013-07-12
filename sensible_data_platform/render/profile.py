from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from identity_providers.models import Cas
from .models import *

@login_required
def profile(request):
    values = {}
    values["sensible"] = sensible_profile(request) # TODO: dynamic
    values["cas"] = cas_profile(request)
    return render_to_response('profile.html', values, context_instance=RequestContext(request))


def cas_profile(request):
    cas = {}
    cas["connector"] = {}
    cas["connector"] = platform_config.IDENTITY_PROVIDERS['CAS']['endpoint']
    cas["profile"] = {}

    try:
        user = Cas.objects.get(user=request.user) 
    except Cas.DoesNotExist:
        print "in except"
        return cas


    cas["profile"]["username"] = user.student_id
    cas["profile"]["email"] = user.email
    cas["profile"]["name"] = user.givenName

    return cas

def sensible_profile(request):
    sensible = {}
    sensible["profile"] = {}
    user = request.user
       
    sensible["profile"]["username"] = user.username
    sensible["profile"]["email"] = user.email
    sensible["profile"]["name"] = user.first_name

    return sensible



