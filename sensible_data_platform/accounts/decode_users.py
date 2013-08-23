import json
from django.contrib.auth.models import User
from identity_providers.models import Cas
from .models import Participant

def decode_users_facebook(filename):
	facebook_filled = [x['user'] for x in json.loads(open('/home/sensibleDTU/sensible-data-platform/SensibleData-Platform/sensible_data_platform/accounts/SECURE_students_facebook').read())]
	for line in open(filename):
		line = line.strip()
		user = json.loads(line)['user']
		student = Cas.objects.get(user=Participant.objects.get(pseudonym=user).user)
		has_facebook = False
		if user in facebook_filled: has_facebook = True
		print "%s	%s	%s	%s"%(student.student_id, student.givenName, student.familyName, has_facebook)


def decode_users(filename):
	emails = set()
	for line in open(filename):
		line = line.strip()
		pseudo = line
		email = Participant.objects.get(pseudonym=pseudo).user.email
		emails.add(email)
	for e in emails:
		print e
