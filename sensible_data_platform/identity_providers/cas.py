from django.http import HttpResponse, HttpResponseRedirect
import urllib2
from .models import *
from django.contrib.auth.decorators import login_required	
import json
from django.shortcuts import redirect
import base64
from xml.dom.minidom import parse, parseString
from utils import platform_config, SECURE_platform_config

@login_required
def link(request):
	auth_base_url = platform_config.IDENTITY_PROVIDERS['CAS']['auth_uri']
	service_url = platform_config.PLATFORM_URI+platform_config.IDENTITY_PROVIDERS['CAS']['endpoint']
	ticket = request.GET.get('ticket', '')
	if ticket == '':
		return HttpResponseRedirect(auth_base_url+"/login?service="+service_url+"&renew=true")
	else:
		validation_url = auth_base_url + "/serviceValidate?ticket="+ticket+"&service="+service_url
		response_auth = urllib2.urlopen(validation_url).read()
		if "cas:authenticationSuccess" in response_auth:
			student_id = response_auth.split("<cas:user>")[1].split("</cas:user>")[0]
			response = saveStudentId(request.user, student_id)
			if 'ok' in response:
				student_attributes = getStudentAttributes(student_id)
				if len(student_attributes) == 1: 
					response = saveStudentAttributes(student_id, student_attributes[0])
			

		else: return HttpResponseRedirect(auth_base_url+"/login?service="+service_url)
	#TODO> pass the response to profile so we can inform the user about the operation
#	return HttpResponse(json.dumps(response))
	return redirect('profile')

def saveStudentId(user, student_id):
	users = User.objects.filter()
	found_users = set()
	for u in users:
		try:
			if u.cas.student_id == student_id: 
				found_users.add(u)
		except Cas.DoesNotExist: continue

	if len(found_users) > 1:
		return {"error": "user with student id already exists %s"%str(found_users)}

	try:
		student = Cas.objects.get(user=user)
		student.student_id = student_id
		student.save()
	except Cas.DoesNotExist:
		student = Cas.objects.create(user=user, student_id=student_id)

	return {"ok": "student id linked"}

def saveStudentAttributes(student_id, attributes):
        student = Cas.objects.get(student_id = student_id)
	student.email = attributes['email']
	student.givenName = attributes['givenName']
	student.familyName = attributes['familyName']
	student.closed = attributes['closed']
	student.save()
	return student.student_id
	

def getStudentAttributes(student_id):
        app_name = SECURE_platform_config.IDENTITY_PROVIDERS['CAS']['app_name']
        app_token = SECURE_platform_config.IDENTITY_PROVIDERS['CAS']['app_token']
        base64string = base64.encodestring('%s:%s' % (SECURE_platform_config.IDENTITY_PROVIDERS['CAS']['requestor'], SECURE_platform_config.IDENTITY_PROVIDERS['CAS']['requestor_password'])).replace('\n', '')
        request = urllib2.Request("https://www.campusnet.dtu.dk/data/CurrentUser/Users/Search?query=%s&first=&amount="%student_id)
        request.add_header("Authorization", "Basic %s"%base64string)
        request.add_header("X-appname", app_name)
        request.add_header("X-token", app_token)
        response = urllib2.urlopen(request).read()
        dom = parseString(response)
        users = []
        for node in dom.childNodes:
                if not node.localName == 'ArrayOfUsers': continue
                for u in node.childNodes:
                        user = {}
                        try:
                                user['email'] = u.attributes['Email'].value
                        except KeyError: pass
                        try:
                                user['givenName'] = u.attributes['GivenName'].value
                        except KeyError: pass
                        try:
                                user['familyName'] = u.attributes['FamilyName'].value
                        except KeyError: pass
                        try:
                                user['closed'] = u.attributes['Closed'].value
                        except KeyError: pass

                        users.append(user)

        return users

