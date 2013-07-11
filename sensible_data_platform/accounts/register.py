from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User

from openid_provider.models import *
from .models import *

from collections import defaultdict
import hashlib

import bson.json_util as json

import utils.user_db as user_db


def check_username(request):
    username = None
    status = None
    description = None

    if request.method == "GET":
        username = request.GET.get("username")

# TODO: sanitize input
# Check is username contains only Capital, small and good symbols, no spaces, no....

        if len(username) < 6 :
            status = -1
            description = "Username must be at lest 6 characters"
        else :
            if user_db.username_taken(username) :
                status = -2
                description = "Username already taken"

            else :
                status = 0
                description = "Username free for selection"

        return HttpResponse(json.dumps({status, description})) # If here everything ok
    
    return HttpResponse(json.dumps("Request method not allowed")) # Should NOT reach this point

def register(request):

	if request.method == 'GET':
		values = defaultdict(dict)
		values['username']['label_tag'] = 'username'
		values['username']['input'] = '<input type="text" name="username" />'
		values['password']['label_tag'] = 'password'
		values['password']['input'] = '<input type="text" name="password" />'
		values['password_repeat']['label_tag'] = 'repeat password'
		values['password_repeat']['input'] = '<input type="text" name="password_repeat" />'
		values['next'] = request.REQUEST.get('next', '')
		values.update(csrf(request))

		return render_to_response('registration/register.html', values)
	
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		next = request.POST.get('next', '')

		#TODO> validate username

		user = User.objects.create_user(username, '', password)

		openid = OpenID()
		openid.user = user
		openid.default = True
		openid.save()

		participant = Participant()
		participant.user = user
		participant.pseudonym = str(hashlib.sha1(user.username).hexdigest())[:30]
		participant.save()

		return redirect(next)



