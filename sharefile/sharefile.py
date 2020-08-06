import requests
from . import utils
from urllib.parse import urljoin

class Sharefile:
    token = None

    def __init__(self, hostname, token):
        self.token = token #utils.auth(hostname, client_id, client_secret, username, password)
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


    def get_by_path(self, path):
        """ Get a single Item by Id.
        Args:
        string item_id - an item id """
        if not self.token:
            raise Exception("Authentication token not present.")
        uri = urljoin(self.hostname, '/sf/v3/Items/ByPath?path={}'.format(path))
        response = requests.get(uri, headers=self.construct_auth_header())
        utils.handle_response(response)
        return response.json()


    def get_children(self, item_id):
        """ Get a single Item by Id.
        Args:
        string item_id - an item id """
        if not self.token:
            raise Exception("Authentication token not present.")
        uri = urljoin(self.hostname, '/sf/v3/Items({})/Children'.format(item_id))
        response = requests.get(uri, headers=self.construct_auth_header())
        utils.handle_response(response)
        return response.json()


    def get_by_tree(self, item_id):
        """ Get a single Item by Id, in tree view.
        Args:
        string item_id - an item id """
        if not self.token:
            raise Exception("Authentication token not present.")
        uri = urljoin(self.hostname, '/sf/v3/Items({itemid})?treemode=mode&sourceId={itemid}&canCreateRootFolder=false'.format(itemid=item_id))
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
        if response.status_code != 204:
            raise Exception("Error deleting object {}\n Code: {}\n Error: {}".format(item_id, response.status_code, response.text))
        return True