from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from oauth2app.models import Client, AccessRange



@login_required
def logout(request):
    auth.logout(request)
    return render_to_response(
        'logout.html',
        {},
        RequestContext(request))
