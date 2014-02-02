from identity_providers.models import Cas
from django.conf import settings
import json

def checkWhitelist(user, client):
	if client.name == 'SensibleDTU':
		try: white_list = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_whitelist').read())
		except: return True
		
		try: white_list_semester_3_4 = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_whitelist_semsester_3_4').read())
		except: pass
		
		try: white_list_semester_5_6 = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_whitelist_semsester_5_6').read())
		except: pass
		

		try: white_list_ku = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_whitelist_ku').read())
		except: pass

		researcher_whitelist = []
		try: 
			researcher_whitelist = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_research_whitelist').read())
		except: pass

		try: 
			if user.email in researcher_whitelist: return True
		except: pass
		
		developer_whitelist = []
		try: 
			developer_whitelist = json.loads(open(settings.ROOT_DIR+'service_manager/SECURE_'+client.name+'_developer_whitelist').read())
		except: pass

		try: 
			if user.email in developer_whitelist: return True
		except: pass
		
		try: 
			if user.email in white_list_ku: return True
		except: pass

		try: user.cas.student_id
		except Cas.DoesNotExist: return False
		
		
		if user.cas.student_id in white_list: return True
		if user.cas.student_id in white_list_semester_3_4: return True
		if user.cas.student_id in white_list_semester_5_6: return True
		
		return False
	return True #no whitelist registered, allow everyone
