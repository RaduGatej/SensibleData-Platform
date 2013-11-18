from django.contrib.auth.views import login
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext

from sensible_platform_documents.get_documents import getText
import accounts_social


@csrf_protect
@never_cache
def authenticate(request):
    text = {}
    text['welcome'] = getText('welcome_text', request.LANGUAGE_CODE)
    
    return render_to_response('social_index.html', {
                'text': text,
                'social_providers': accounts_social.getSocialProviders()
            }, context_instance=RequestContext(request))