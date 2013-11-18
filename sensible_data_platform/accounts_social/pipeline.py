
# from social.pipeline.partial import partial

from accounts.register import _register

def register(strategy, details, response, uid, user=None, *args, **kwargs):
    if user:
        return

    return {
        'is_new': True,
        'user': _register(details['email'])
    }

