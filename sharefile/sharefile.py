import requests
from . import utils
from urllib.parse import urljoin

class Sharefile:
    token = None

    def __init__(self, hostname, client_id, client_secret, username, password):
        self.token = utils.auth(hostname, client_id, client_secret, username, password)
        self.hostname = hostname


    def construct_auth_header(self):
        return {'Authorization':'Bearer {}'.format(self.token)}


    def get_by_id(self, item_id):
        """ Get a single Item by Id.
        Args:
        string item_id - an item id """
        if not self.token:
            raise Exception("Authentication token not present.")
        uri = urljoin(self.hostname, '/sf/v3/Items({})'.format(item_id))
        response = requests.get(uri, headers=self.construct_auth_header())
        utils.handle_response(response)
        return response.json()


    def delete_item(self, item_id):
        """ Delete an Item by Id.
        Args:
        string item_id - the id of the item to delete """
        if not self.token:
            raise Exception("Authentication token not present.")
        uri = urljoin(self.hostname, '/sf/v3/Items({})'.format(item_id))
        response = requests.delete(uri, headers=self.construct_auth_header())
        if response.status_code != 200:
            raise Exception("Error deleting object {}".format(item_id))
        return response.json()