from django.contrib.auth.views import login
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext

from sensible_platform_documents.get_documents import getText

@sensitive_post_parameters()
@csrf_protect
@never_cache
def do_login(request):
	trust_root = request.REQUEST.get('trust_root', '')
	return login(request, extra_context={'trust_root':trust_root})

@csrf_protect
@never_cache
def authenticate(request):
    text = {}
    text['welcome'] = getText('welcome_text', request.LANGUAGE_CODE)
    return render_to_response('index.html', {'text': text}, context_instance=RequestContext(request))