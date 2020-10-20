#!/usr/bin/env python3
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
		print("Found {} folders.".format(len(all_folders["value"])))
		for i in all_folders["value"]:
			if i["Name"] == "_Reports":
				reportUID = i["Id"]
				pass
			if i["FileCount"] == 0 and i["Name"] != "_Reports":
				dateDifference = (datetime.datetime.now() - parser.parse(i['CreationDate']).replace(tzinfo=None)).days
				outString = "Found Empty Folder With Name: {}, ID: {}, Size: {}\n".format(i["Name"], i["Id"], i["FileCount"])
				if dateDifference > 14:
					if VERBOSE:
						print(outString)
					f.write(outString)
					try:
						if client.delete_item(i["Id"]):
							if VERBOSE:
								print("Successfully Deleted")
						delete_count += 1
					except KeyboardInterrupt:
						print("ctrl + c - Exiting")
						exit()
					except:
						outstring = "Error deleting {} : {}".format(i["Id"], i["Name"])
						if VERBOSE:
							print(outstring)
						f.write(outstring)
				else:
					if VERBOSE:
						print("Skipping folder, created less than 15 days ago.")
		if delete_count:
			print("Deleted {} items.".format(delete_count))
	print("Uploading log..")
	client.upload_item(reportUID, "/tmp/"+OUTFILE+"_"+sys.argv[1], OUTFILE)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("This script removes all empty folders.")
		print("USAGE:\n Environment Variables: \nSF_URL (ShareFile URL)\nSF_CID (Sharefile Client ID)\nSF_CS (Sharefile Client Secret)\nSF_USER (Sharefile service account username)\nSF_PWD (Sharefile user password)\n ./deleteEmptyFolders.py <parent folder ID item_id>")
		exit()
	try:
		main()
	except KeyboardInterrupt:
		print("ctrl + c - Exiting")
		exit()
