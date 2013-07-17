from oauth2app.models import *

def clientAuthorizations(client, user):
	authorizations = AccessToken.objects.filter(client=client, user=user).all()
	ass = []
	for a in authorizations:
		ass += [k.key for k in a.scope.all()]
	return ass

def getClients(user, type):
	clients = Client.objects.filter(type=ClientType.objects.get(type=type))
	return clients
	
def getTokenForUser(client, user, scope):
	token = AccessToken.objects.filter(client=client, user=user, scope=AccessRange.objects.get(key=scope)).order_by('-issue')
	try: t = token[0].token
	except IndexError: t = {'error':'does not exist'}
	except AccessToken.DoesNotExist: t = {'error':'does not exist'}
	except Scope.DoesNotExist: t = {'error':'does not exist'}

	return t

def getEndpoint(resource, client):
	return client.api_uri+resource+'/'
