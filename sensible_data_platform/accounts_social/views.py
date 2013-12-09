from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext

from sensible_platform_documents.get_documents import getText
import accounts_social
from social.apps.django_app.default.models import UserSocialAuth
from render.profile import sensible_profile, profile as _profile


@csrf_protect
@never_cache
def authenticate(request):
    text = {}
    text['welcome'] = getText('welcome_text', request.LANGUAGE_CODE)
    
    return render_to_response('social/index.html', {
                'text': text,
                'social_providers': accounts_social.getSocialProviders()
            }, context_instance=RequestContext(request))


@csrf_protect
@login_required
def profile(request):
    if request.method == 'POST':
        return _profile(request)
    else:
        values = {}
        values["sensible"] = sensible_profile(request, values)

        return render_to_response('social/profile.html', values, context_instance=RequestContext(request))