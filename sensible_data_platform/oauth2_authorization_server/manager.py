from oauth2app.models import *

def clientAuthorizations(client, user):
	authorizations = AccessToken.objects.filter(client=client, user=user).all()
	ass = []
	for a in authorizations:
		ass += [k.key for k in a.scope.all()]
	return ass

def getClients(user):
	#TODO: whiteslist
	clients = Client.objects.filter()
	return clients
	
def getTokenForUser(client, user):
	token = AccessToken.objects.filter(client=client, user=user).order_by('-issue')
	try: t = token[0].token
	except IndexError: t = None	
	return t

def getEndpoint(resource, client):
	return client.api_uri+resource+'/'
