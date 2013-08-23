from identity_providers.models import Cas
from django.conf import settings
import json

def checkWhitelist(user, client):
	if client.name == 'SensibleDTU':
		try: white_list = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_whitelist').read())
		except: return True
		
		researcher_whitelist = []
		try: 
			researcher_whitelist = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_research_whitelist').read())
		except: pass

		try: 
			if user.email in researcher_whitelist: return True
		except: pass

		try: user.cas.student_id
		except Cas.DoesNotExist: return False
		
		
		if user.cas.student_id in white_list: return True
		
		return False
	return True #no whitelist registered, allow everyone
