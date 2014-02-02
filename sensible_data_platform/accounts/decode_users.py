import json
from django.contrib.auth.models import User
from identity_providers.models import Cas
from .models import Participant
from collections import defaultdict

def decode_users_facebook(filename):
	facebook_filled = [x['user'] for x in json.loads(open('/home/sensibleDTU/sensible-data-platform/SensibleData-Platform/sensible_data_platform/accounts/SECURE_students_facebook').read())]
	for line in open(filename):
		line = line.strip()
		user = json.loads(line)['user']
		student = Cas.objects.get(user=Participant.objects.get(pseudonym=user).user)
		has_facebook = False
		if user in facebook_filled: has_facebook = True
		print "%s	%s	%s	%s"%(student.student_id, student.givenName, student.familyName, has_facebook)


def decode_users_emails(filename):
	emails = set()
	for line in open(filename):
		line = line.strip()
		pseudo = line
		email = Participant.objects.get(pseudonym=pseudo).user.email
		emails.add(email)
	for e in emails:
		print e

def decode_users_with_devices(filename):
	emails = set()
	for line in open(filename):
		line = line.strip()
		student_id = line
		student = Cas.objects.filter(student_id = student_id)
		#if not len(student) == 1:
		for x in student:
			emails.add(x.email)
			emails.add(x.user)


	for e in emails: print e

def decode_users_with_devices_2(filename):
	emails = defaultdict(str)
	students_with_devices = set()
	for line in open(filename):
		line = line.strip()
		vs = line.split('\t')
		vs[0] = 's'+vs[0].zfill(6)
		if len(vs) > 1 and emails[vs[0]] == '': emails[vs[0]] = vs[-1]

	for line in open('/home/sensibleDTU/sensible-data-platform/SensibleData-Platform/sensible_data_platform/accounts/SECURE_students_with_devices'):
		line = line.strip()
		students_with_devices.add(line)

	for s in emails:
		if s in students_with_devices: continue
		print '%s@student.dtu.dk'%s
		print emails[s]

def decode_users(filename):
	for line in open(filename):
		line = line.strip()
		vs = line.split('\t')
		user = Participant.objects.get(pseudonym=vs[0]).user

		try: 
			student = Cas.objects.get(user=user)
			print "%s \t %s \t %s \t %s \t %s"%(student.givenName, student.familyName, student.student_id, user.email, vs[1])
		except: 
			print "%s \t %s \t %s \t %s \t %s"%("NO CAS?!", "NO CAS?!", "NO CAS?!", user.email, vs[1])
