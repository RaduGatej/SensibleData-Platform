from django.core.context_processors import csrf
from django.contrib.auth.models import User
from social.apps.django_app.utils import BACKENDS
from social.backends import utils as social_utils
from itertools import chain

## 
# A dict with backend names and "pretty" names
# The backend names can be found in social.backends.<X>.<Class>.name
backend_translation = {
    'facebook':      {'name': 'Facebook', 'icon': 'facebook',   'btnstyle':'facebook'},
    'twitter':       {'name': 'Twitter',  'icon': 'twitter',    'btnstyle':'twitter'},
    'google-oauth2': {'name': 'Google',   'icon': 'googleplus', 'btnstyle':'google'},
}

##
# Returns the name, icon and button style of the active backends
def getSocialProviders():
    backends = social_utils.load_backends(BACKENDS)
    return [dict(chain({'backend': backend}.iteritems(), backend_translation[backend].iteritems())) for backend in backends]