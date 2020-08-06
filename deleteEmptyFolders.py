#!/usr/bin/env python3
from sharefile.sharefile import Sharefile
import os
import sys

def main():
	try:
		client = Sharefile(os.environ["SF_URL"], os.environ["SF_TOKEN"])
	except KeyError:
		raise Exception("Environment Variables Not Set.")
		exit()

	all_folders = client.get_children(sys.argv[1])
	delete_count = 0
	for i in all_folders["value"]:
		if i["FileCount"] == 0 and i["Name"] != "_Reports":
			print("Found Empty Folder With Name: {}, ID: {}, Size: {}".format(i["Name"], i["Id"], i["FileCount"]))
			if client.delete_item(i["Id"]):
				print("Successfully Deleted")
			delete_count += 1
	if delete_count:
		print("Deleted {} items.".format(delete_count))
		exit()
	print("Found no items to delete.")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("USAGE:\n Environment Variables: SF_URL (ShareFile URL), SF_TOKEN (ShareFile Oauth2 Token)\n ./deleteEmptyFolders.py <parent folder ID item_id>")
		exit()
	main()