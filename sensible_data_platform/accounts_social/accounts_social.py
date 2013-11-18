from django.core.context_processors import csrf
from django.contrib.auth.models import User
from social.apps.django_app.utils import BACKENDS
from social.backends import utils as social_utils
# from identity_providers.models import Cas

# from openid_provider.models import *


# def getUser(user):
# 	values = {}
# 	values['username'] = str(user)
	
# 	try:
# 		student = Cas.objects.get(user=user) 
# 		values['student_id'] = str(student.student_id)
# 	except Cas.DoesNotExist: pass
	
# 	return values

## A dict with backend names and "pretty" names
backend_translation = {
    'facebook':      'Facebook',
    'facebook-app':  'Facebook',
    'twitter':       'Twitter',
    'google-oauth2': 'Google',
}

def getSocialProviders():
    backends = social_utils.load_backends(BACKENDS)
    return [{'backend': backend, 'name': backend_translation[backend]} for backend in backends]