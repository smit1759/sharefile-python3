from sharefile.sharefile import Sharefile
import os

def main():
	client = Sharefile(os.environ["SF_URL"], os.environ["SF_CI"], os.environ["SF_CS"], os.environ["SF_USR"], os.environ["SF_PWD"])
	print(client.get_by_id("fof6f3e6-5e20-4e6c-8b35-8f4a26340e4d"))
	return None


if __name__ == "__main__":
	main()