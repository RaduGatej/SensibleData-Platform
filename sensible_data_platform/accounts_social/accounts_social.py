from django.core.context_processors import csrf
from django.contrib.auth.models import User
from social.apps.django_app.utils import BACKENDS
from social.backends import utils as social_utils
from itertools import chain

## A dict with backend names and "pretty" names
backend_translation = {
    'facebook':      {'name': 'Facebook', 'icon': 'facebook',   'btnstyle':'facebook'},
    'twitter':       {'name': 'Twitter',  'icon': 'twitter',    'btnstyle':'twitter'},
    'google-oauth2': {'name': 'Google',   'icon': 'googleplus', 'btnstyle':'google'},
}

def getSocialProviders():
    backends = social_utils.load_backends(BACKENDS)
    return [dict(chain({'backend': backend}.iteritems(), backend_translation[backend].iteritems())) for backend in backends]