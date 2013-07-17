from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from accounts import manager
from utils import platform_config
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from identity_providers.models import Cas
from .models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from accounts.models import Extra

@login_required
def profile(request):
    if request.method == 'GET':
        values = {}
        values["cas"] = cas_profile(request)
        values["sensible"] = sensible_profile(request, values) # TODO: dynamic
        values['platformUri'] = platform_config.PLATFORM_URI

        return render_to_response('profile.html', values, context_instance=RequestContext(request))

    if request.method == 'POST':
        username = request.user
        user = User.objects.get(username__exact=username) # TODO: sanitize input server-side
        user.email = request.POST.get("email_field", "")
        user.first_name = request.POST.get("first_name_field", "")
        user.last_name = request.POST.get("last_name_field", "")
        user.save()


        extra = None
        try: extra = Extra.objects.get(user = request.user)
        except Extra.DoesNotExist: extra = Extra.objects.create(user = request.user)

        extra.phone = request.POST.get("phone_field", "")
        extra.save()

        return redirect('profile.html', context_instance=RequestContext(request))


def sensible_profile(request, values):
    sensible = {}
    sensible["profile"] = {}
    user = request.user
       
    sensible["profile"]["username"] = user.username
    sensible["profile"]["email"] = user.email

    if user.first_name ==  "" and len(values["cas"]["profile"]) != 0  :
        user.first_name = values["cas"]["profile"]["givenName"]
    sensible["profile"]["first_name"] = user.first_name

    if user.last_name ==  ""  and len(values["cas"]["profile"]) != 0:
        user.last_name = values["cas"]["profile"]["familyName"]
    sensible["profile"]["last_name"] = user.last_name


    extra = None
    try:
        extra = Extra.objects.get(user__exact = request.user)
    except Extra.DoesNotExist:
        print "Extra does not exists"
        user.save()
        return sensible

    sensible["profile"]["phone"] = extra.phone

    return sensible


def cas_profile(request):
    cas = {}
    cas["connector"] = {}
    cas["connector"] = platform_config.IDENTITY_PROVIDERS['CAS']['endpoint']
    cas["profile"] = {}

    try:
        user = Cas.objects.get(user=request.user) 
    except Cas.DoesNotExist:
        print "No CAS profile"
        return cas

    cas["profile"]["username"] = user.user
    cas["profile"]["student_id"] = user.student_id
    cas["profile"]["email"] = user.email
    cas["profile"]["givenName"] = user.givenName
    cas["profile"]["familyName"] = user.familyName

    return cas

