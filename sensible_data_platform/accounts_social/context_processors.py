from social.apps.django_app.context_processors import LazyDict, backends as _backends

# from itertools import chain

from accounts_social import backend_translation
from django.forms.models import model_to_dict

# from social.backends.utils import user_backends_data

def backends(request):
    return {'backends': LazyDict(lambda: _merge_backend_data(_backends(request)))}

def _merge_backend_data(backends):
    values = {'associated': [], 'not_associated': [], 'old': backends}

    for auth in backends['backends']['associated']:
        value = backend_translation[auth.provider].copy()
        value.update(model_to_dict(auth))
        values['associated'].append(value)

    for auth in backends['backends']['not_associated']:
        value = backend_translation[auth].copy()
        value['provider'] = auth
        values['not_associated'].append(value)

    # return [dict((backend, backend_translation[backend])) for backend in backends]
    return values