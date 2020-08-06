from main import *

class TPN_reupload_thumbnails(TPN_post_problems_bot):
	def __init__(self, email, password, driver):
		self.email = email
		self.password = password
		self.driver = driver

	def __del__(self):
		self.driver.close()

def main():
	email = input('email:')
	password = input('password:')
	
	path = convertToOS("path")

	bot = TPN_reupload_thumbnails(email, password, get_driver(path, options))
	bot.login()


if __name__ == '__main__':
	main()