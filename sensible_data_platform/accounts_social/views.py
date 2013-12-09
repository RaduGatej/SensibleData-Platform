from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext

from sensible_platform_documents.get_documents import getText
import accounts_social
from social.apps.django_app.default.models import UserSocialAuth

# testing
from django.http import HttpResponse
from pprint import pformat


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
    providers = accounts_social.getSocialProviders()

    # for provider in providers.keys():
    #     providers[provider]['action'] = 'Link to '

    # associations = UserSocialAuth.objects.filter(user=request.user)

    # for association in associations:
    #     providers[association.provider]['action'] = 'disconnect'

    return render_to_response('social/profile.html', {
                'social_providers': providers
            }, context_instance=RequestContext(request))