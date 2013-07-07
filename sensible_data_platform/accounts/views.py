from django.contrib.auth.views import login
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

@sensitive_post_parameters()
@csrf_protect
@never_cache
def do_login(request):
	trust_root = request.REQUEST.get('trust_root', '')
	return login(request, extra_context={'trust_root':trust_root})
