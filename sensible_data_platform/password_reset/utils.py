import smtplib
from django.conf import settings
from ntlm.smtp import ntlm_authenticate
from email.mime.text import MIMEText as text

try:
	from django.contrib.auth import get_user_model
except ImportError:
	from django.contrib.auth.models import User
	get_user_model = lambda: User  # noqa


def get_username(user):
	username_field = getattr(user, 'USERNAME_FIELD', 'username')
	return getattr(user, username_field)

def send_email(receiver_email, message, subject=""):
	username = settings.EMAIL_HOST_USER
	password = settings.EMAIL_HOST_PASSWORD

	#server = smtplib.SMTP(settings.EMAIL_HOST + ":" + str(settings.EMAIL_PORT))
	#server.starttls()
	server = smtplib.SMTP()
	server.connect(settings.EMAIL_HOST, settings.EMAIL_PORT)
	server.ehlo()
	server.starttls()
	#server.login(username, password)
	#ntlm_authenticate(server, username, password)

	fromaddr = settings.DEFAULT_FROM_EMAIL
	toaddrs  = receiver_email

	m = text(message.encode('utf-8'),'plain','utf-8')

	m['Subject'] = subject
	m['From'] = fromaddr
	m['To'] = toaddrs

	print server.sendmail(fromaddr, toaddrs, m.as_string())
	server.quit()
