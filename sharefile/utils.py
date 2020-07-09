import requests
from urllib.parse import urljoin


def auth(hostname, client_id, client_secret, username, password):
	uri = urljoin(hostname, '/oauth/token')
	headers = {
	'Content-Type': 'application/x-www-form-urlencoded'
	}
	params = {
		'grant_type': 'password',
		'client_id': client_id,
		'client_secret': client_secret,
		'username': username,
		'password': password
	}
	response = requests.post(uri, params=params, headers=headers)
	print(response.status_code, response.json())
	if response.status_code != 200:
		raise Exception("[!] Error gaining oauth token")
	return response.json()


def handle_response(response):
	if response.status_code == 404:
		raise Exception("Item not found")
	elif response.status_code == 401:
		raise Exception("Unauthorized")
	elif response.status_code == 400:
		raise Exception("Bad request")
	elif response.status_code != 200:
		raise Exception("Other error")
	else:
		pass
