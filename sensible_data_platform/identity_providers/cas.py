from django.http import HttpResponse, HttpResponseRedirect
import urllib2
from .models import *
from django.contrib.auth.decorators import login_required	
import json
from django.shortcuts import redirect
import base64
from xml.dom.minidom import parse, parseString
from utils import platform_config, SECURE_platform_config

from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

@login_required
def link(request):
	values = {}
	values['profilePage'] = settings.BASE_URL + "profile/"
	auth_base_url = platform_config.IDENTITY_PROVIDERS['CAS']['auth_uri']
	service_url = request.build_absolute_uri(reverse('id_cas'))
	ticket = request.GET.get('ticket', '')
	if ticket == '':
		return HttpResponseRedirect(auth_base_url+"/login?service="+service_url+"&renew=true")
	else:
		validation_url = auth_base_url + "/serviceValidate?ticket="+ticket+"&service="+service_url
		response_auth = urllib2.urlopen(validation_url).read()
		if "cas:authenticationSuccess" in response_auth:
			student_id = response_auth.split("<cas:user>")[1].split("</cas:user>")[0]
			response = checkCas(request.user, student_id)
			values['response'] = response
			if 'ok' in response["status"]:
				student_attributes = getStudentAttributes(student_id)
				if len(student_attributes) == 1: 
					response = saveStudentAttributes(student_id, student_attributes[0])
		        else :
					r = redirect('home')
					r['Location'] += '?status=failed&message='+response['message']
					return r
		else: return HttpResponseRedirect(auth_base_url+"/login?service="+service_url)
		
		
		
	r = redirect('home')
	r['Location'] += '?status=success&message=Profile linked!'
	return r

def checkCas(user, student_id):
	users = User.objects.filter()
	found_users = set()
	for u in users:
		try: 
			if u.cas.student_id == student_id: 
				found_users.add(u)
		except Cas.DoesNotExist: continue

	if len(found_users) > 0:
		return {"status" : "error", "message" :  "User with student id <%s> already exists."%str(student_id)}
	
	try: student = Cas.objects.get(student_id = student_id)
	except Cas.DoesNotExist: 
		try:
			student = Cas.objects.create(user=user, student_id=student_id)
			student.student_id = student_id
			student.save()
		except: return {"status" : "error", "message" : "something went wrong, please try again"}

	except Cas.MultipleObjectsReturned:
		return {"status" : "error", "message" : "user with student id already exists %s"%str(student_id)}
	return {"status" : "ok", "message" : "student id linked"}

def saveStudentAttributes(student_id, attributes):
        try:
            student = Cas.objects.get(student_id = student_id)
        except Cas.MultipleObjectsReturned as e:
            return render_to_response('profile.html', {"status" : "error", "message" : "user with student id already exists %s"%str(student_id)}, context_instance=RequestContext(request))

	student.email = attributes['email']
	student.givenName = attributes['givenName']
	student.familyName = attributes['familyName']
	student.closed = attributes['closed']
	student.save()

	if student.user.first_name == '':
		student.user.first_name = attributes['givenName']
		student.user.save()
	if student.user.last_name == '':
		student.user.last_name = attributes['familyName']
		student.user.save()

	return student.student_id
	

def getStudentAttributes(student_id):
	app_name = SECURE_platform_config.IDENTITY_PROVIDERS['CAS']['app_name']
	app_token = SECURE_platform_config.IDENTITY_PROVIDERS['CAS']['app_token']
	base64string = base64.encodestring('%s:%s' % (SECURE_platform_config.IDENTITY_PROVIDERS['CAS']['requestor'], SECURE_platform_config.IDENTITY_PROVIDERS['CAS']['requestor_password'])).replace('\n', '')
	request = urllib2.Request("https://www.campusnet.dtu.dk/data/CurrentUser/Users/Search?query=%s&first=&amount="%student_id)
	request.add_header("Authorization", "Basic %s"%base64string)
	request.add_header("X-appname", app_name)
	request.add_header("X-token", app_token)
	users = []
	try:
		response = urllib2.urlopen(request).read()
	except urllib2.HTTPError:
		return users
	dom = parseString(response)
	for node in dom.childNodes:
		if not node.localName == 'ArrayOfUsers': continue
		for u in node.childNodes:
			user = {}
			try: user['email'] = u.attributes['Email'].value
			except KeyError: pass
			try: user['givenName'] = u.attributes['GivenName'].value
			except KeyError: pass
			try: user['familyName'] = u.attributes['FamilyName'].value
			except KeyError: pass
			try: user['closed'] = u.attributes['Closed'].value
			except KeyError: pass
			users.append(user)

	if len(users) == 1: return users

	final_users = []
	for user in users:
		if not user['closed'] == 'false': continue
		if not student_id in user['email']: continue
		final_users.append(user)

	return final_users
