import requests
from . import utils
from urllib.parse import urljoin
from urllib.parse import urlparse
import os
import time
import mimetypes
import http 


class Sharefile:
    token = None

    def __init__(self, hostname=None, client_id=None, client_secret=None, username=None, password=None, token=None):
        if token:
            self.token = token
        else:
            self.token = utils.auth(hostname, client_id, client_secret, username, password)["access_token"]
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
        string path - an path """
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

    def upload_item(self, folder_id, file_loc, file_name):
        """ Upload an item to a folder by Id.
        Args:
        string item_data - the data of the item to upload """
        if not self.token:
            raise Exception("Authentication token not present.")
        params = {
            "method": "standard",
            "raw": "true",
            "fileName": file_name

        }
        uri = urljoin(self.hostname, '/sf/v3/Items({})/Upload'.format(folder_id))
        upload_uri = requests.get(uri, params=params, headers=self.construct_auth_header())
        if upload_uri.status_code != 200:
            raise Exception("Error uploading object {}\n Code: {}\n Error: {}".format(folder_id, upload_uri.status_code, upload_uri.text))
        data = open(file_loc,'rb')
        r = requests.post(upload_uri.json()['ChunkUri'], data=data)
        print(r.text)
