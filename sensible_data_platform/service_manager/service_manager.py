from oauth2_authorization_server import manager
import urllib2
import json
from collections import defaultdict
from oauth2app.models import *

def getResource(resource, client, user):
	token = manager.getTokenForUser(client, user)
	if token == None: return {'error': 'no token available'}
	endpoint = manager.getEndpoint(resource, client)
	url = endpoint+'?access_token='+token
	try: response = urllib2.urlopen(endpoint+'?access_token='+token).read()
	except: response = {'error': 'connection error'}
	
	if type(response) == str: response = json.loads(response)
	return response

def userStatus(client, user):
        #available, initiated, enrolled
	response = getResource('userStatus', client, user)
	if 'error' in response: status = 'unknown'
	else: status = response['user_status']

        if status == 'unknown': status = 'available'
        return status


def getServices(user):
	services = defaultdict(lambda: defaultdict(dict))
        clients = manager.getClients(user)
        for client in clients:
		status = userStatus(client, user)
                services[status][client.name] = {}
                services[status][client.name]['description'] = client.description
                services[status][client.name]['authorizations'] = manager.clientAuthorizations(client, user)
                services[status][client.name]['redirect_uri'] = client.redirect_uri
                services[status][client.name]['client_id'] = client.key
                services[status][client.name]['status'] = status
	
	#TODO: authorizations that the study requests from the config

	for v in services:
		services[v] = dict(services[v])

        return dict(services)

def getAuthorizations(user, services):
	authorizations = {}
	for user_status in services:
		for service in services[user_status]:
			authorizations[service] = getAuthorizationsForService(user, services[user_status][service])


	return authorizations


def getAuthorizationsForService(user, service):
	client = Client.objects.get(key=service['client_id'])
	authorizations = getResource('serviceAuthorizations', client, user)
	return authorizations
