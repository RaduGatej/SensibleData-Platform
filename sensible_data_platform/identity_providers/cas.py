from django.http import HttpResponse, HttpResponseRedirect
import urllib2
from accounts.models import *
from django.contrib.auth.decorators import login_required	
import json


@login_required
def link(request):
	#TODO: make this nicer code, read url from platform_config
	auth_base_url = "https://auth.dtu.dk/dtu"
	service_url = "http://166.78.249.214:8081/identity_providers/cas/"
	ticket = request.GET.get('ticket', '')
	if ticket == '':
		return HttpResponseRedirect(auth_base_url+"/login?service="+service_url+"&renew=true")
	else:
		validation_url = auth_base_url + "/serviceValidate?ticket="+ticket+"&service="+service_url
		response_auth = urllib2.urlopen(validation_url).read()
		if "cas:authenticationSuccess" in response_auth:
			student_id = response_auth.split("<cas:user>")[1].split("</cas:user>")[0]
			response = saveStudentId(request.user, student_id)
		else: return HttpResponseRedirect(auth_base_url+"/login?service="+service_url)
	return HttpResponse(json.dumps(response))

def saveStudentId(user, student_id):

	users = User.objects.filter()
	found_user = None
	for u in users:
		try:
			if u.student.student_id == student_id: 
				found_user = u
				break	
		except Student.DoesNotExist: continue

	if not found_user == user:
		return {"error": "user with student id already exists"}

	try:
		student = Student.objects.get(user=user)
		student.student_id = student_id
	except Student.DoesNotExist:
		student = Student.objects.create(user=user, student_id=student_id)

	return {"ok": "student id linked"}


def getStudentAttributes(student_id):
	pass
	#TODO: seems that we need to scrape http://www.dtu.dk/English/Service/Phonebook.aspx?searchstring=arks@dtu.dk&type=employee
