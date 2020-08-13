#!/usr/bin/env python3
# Add checking of expiry of folder < 7 days old

from sharefile.sharefile import Sharefile
import os
import sys
import datetime
from dateutil import parser

OUTFILE = f"{datetime.datetime.now():sharefile_log_%d_%m_%Y}"
VERBOSE = True

def main():
	try:
		client = Sharefile(hostname=os.environ["SF_URL"], client_id=os.environ["SF_CID"], client_secret=os.environ["SF_CS"], username=os.environ["SF_USER"], password=os.environ["SF_PWD"])
	except KeyError:
		raise Exception("Environment Variables Not Set.")
		exit()

	all_folders = client.get_children(sys.argv[1])
	delete_count = 0
	reportUID = None
	with open("/tmp/"+OUTFILE+"_"+sys.argv[1], "a") as f:
		for i in all_folders["value"]:
			if i["Name"] == "_Reports":
				reportUID = i["Id"]
				continue
			if i["FileCount"] == 0:
				dateDifference = (parser.parse(i['CreationDate']).replace(tzinfo=None) - datetime.datetime.now()).days
				outString = "Found Empty Folder With Name: {}, ID: {}, Size: {}\n".format(i["Name"], i["Id"], i["FileCount"])
				if dateDifference <= 15:
					print(outString)
					print("Skipping folder, created less than 15 days ago.")
					continue
				if VERBOSE:
					print(outString)
				f.write(outString)
				if client.delete_item(i["Id"]):
					print("Successfully Deleted")
				delete_count += 1
		if delete_count:
			print("Deleted {} items.".format(delete_count))
	print("Uploading log..")
	client.upload_item(reportUID, "/tmp/"+OUTFILE+"_"+sys.argv[1], OUTFILE)
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("This script removes all ")
		print("USAGE:\n Environment Variables: SF_URL (ShareFile URL), SF_CID (Sharefile Client ID), SF_CS (Sharefile Client Secret), SF_USER (Sharefile service account username), SF_PWD (Sharefile user password)\n ./deleteEmptyFolders.py <parent folder ID item_id>")
		exit()
	main()