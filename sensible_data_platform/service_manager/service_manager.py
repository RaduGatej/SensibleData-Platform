from oauth2_authorization_server import manager
import urllib2
import json
from collections import defaultdict
from oauth2app.models import *
import whitelist
from django.core.urlresolvers import reverse
import urllib2

#depricated
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



#deprecated
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

def getServices2(user,language):
	services = {}
	clients = manager.getClients('study')
	for client in clients:
		if not whitelist.checkWhitelist(user, client): continue
		discovery = discoverService(client,language)
		services[client.name] = {}
		token = manager.getTokenForUser(client=client, user=user, scope='enroll')

		if 'error' in token: 
			services[client.name]['error'] = 'unauthorized_no_token'
			services[client.name]['authorize_url'] = client.authorize_uri
			services[client.name]['discovery'] = discovery
			continue

		status = getUserStatus(client, token)
		if 'error' in status: 
			services[client.name]['error'] = status['error']
			services[client.name]['authorize_url'] = client.authorize_uri
			services[client.name]['discovery'] = discovery
			continue
		services[client.name] = status
		services[client.name]['discovery'] = discovery

	return services

def discoverService(client,language):
	#TODO set service to 'offline' if there is an error
	url = client.api_uri + 'discover/?language='+language
	try:response = urllib2.urlopen(url).read()
	except urllib2.HTTPError: return {'error':'connection refused'}
	except urllib2.URLError: return {'error':'connection refused'}
	try: response = json.loads(response)
	except ValueError: return {'error':'connection refused'}
	return response

def getInformedConsent(client,language):
	url = client.api_uri + 'informed_consent/?language='+language
	response = urllib2.urlopen(url).read()
	return json.loads(response)

def getUserStatus(client, token):
	url = client.api_uri+'userStatus/'
	url += '?access_token='+token
	try: response = urllib2.urlopen(url).read()
	except: response = {'error': 'connection error'}
	
	if type(response) == str: response = json.loads(response)
	return response

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



