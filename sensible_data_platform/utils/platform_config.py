#PLATFORM_URI = 'https://www.sensible.dtu.dk/sensible-data'
PLATFORM_URI = 'http://166.78.249.214:9081'


IDENTITY_PROVIDERS = {
	'CAS':	{
		'connector': 'cas.py',
		'auth_uri': 'https://auth.dtu.dk/dtu/',
		'endpoint': '/identity_providers/cas/',
	}
}
