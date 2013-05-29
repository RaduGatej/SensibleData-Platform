from django.core.context_processors import csrf
from django.contrib.auth.models import User
from accounts.models import Cas

from openid_provider.models import *


def getUser(user):
	values = {}
	values['username'] = str(user)
	
	try:
		student = Cas.objects.get(user=user) 
		values['student_id'] = str(student.student_id)
	except Cas.DoesNotExist: pass
	
	return values
