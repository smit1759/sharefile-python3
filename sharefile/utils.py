import requests
from urllib.parse import urljoin
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

def auth(hostname, client_id, client_secret, username, password):
	try:
		oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
		token = oauth.fetch_token(token_url=urljoin(hostname, '/oauth/token'),
	        username=username, password=password, client_id=client_id,
	        client_secret=client_secret)
		return token
	except Exception as e:
		raise Exception("[!] Error gaining oauth token:\n{0}".format(e))


def handle_response(response):
	if response.status_code == 404:
		raise Exception("Item not found: {}".format(response.text))
	elif response.status_code == 401:
		raise Exception("Unauthorized: {}".format(response.text))
	elif response.status_code == 400:
		raise Exception("Bad request: {}".format(response.text))
	elif response.status_code != 200:
		raise Exception("Other error: {}".format(response.text))
	else:
		pass
