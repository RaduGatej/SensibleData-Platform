from identity_providers.models import Cas
from django.conf import settings
import json

def checkWhitelist(user, client):
	if client.name == 'SensibleDTU':
		try: user.cas.student_id
		except Cas.DoesNotExist: return False
		
		try: white_list = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_whitelist').read())
		except: return True
		
		if user.cas.student_id in white_list: return True
		
		return False
