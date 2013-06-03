from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User

from openid_provider.models import *
from .models import *

from collections import defaultdict
import hashlib

def register(request):

	if request.method == 'GET':
		values = defaultdict(dict)
		values['username']['label_tag'] = 'username'
		values['username']['input'] = '<input type="text" name="username" />'
		values['password']['label_tag'] = 'password'
		values['password']['input'] = '<input type="text" name="password" />'
		values['password_repeat']['label_tag'] = 'repeat password'
		values['password_repeat']['input'] = '<input type="text" name="password_repeat" />'
		values.update(csrf(request))


		return render_to_response('registration/register.html', values)
	
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		#TODO> validate username

		user = User.objects.create_user(username, '', password)

		openid = OpenID()
		openid.user = user
		openid.default = True
		openid.save()

		participant = Participant()
		participant.user = user
		participant.pseudonym = str(hashlib.sha1(user.username).hexdigest())
		participant.save()

		return HttpResponse(username+' created successfully!')
