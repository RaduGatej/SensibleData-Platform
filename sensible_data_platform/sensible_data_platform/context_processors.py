from django.conf import settings
import os

def platform(request):
    path = os.path.abspath(os.path.join(settings.ROOT_DIR,"..","VERSION"))
    with open(path) as f:
        version = f.read()
    is_devel = '-devel' in version

    return {'platform':{'name':settings.PLATFORM_NAME, 'version':version, 'is_devel':is_devel}, 'support_email': settings.SUPPORT_EMAIL}
