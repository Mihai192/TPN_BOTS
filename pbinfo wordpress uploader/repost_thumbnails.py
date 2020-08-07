from main import *

class TPN_reupload_thumbnails(TPN_post_problems_bot):
	def __init__(self, email, password, driver):
		self.email = email
		self.password = password
		self.driver = driver

	def get_num_of_pages(self):
		num_of_pages_element = WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.CLASS_NAME, 'total-pages')))
		return	int(num_of_pages_element.get_attribute('innerHTML'))

	# post --> tr
	def has_thumbnail(self, post):
		try:
			WebDriverWait(post, 3).until(ec.visibility_of_element_located((By.TAG_NAME, 'img')))
			return True
		except Exception:
			return False

	def get_problem_id(self, post):
		text = WebDriverWait(post, 20).until(ec.visibility_of_element_located((By.CLASS_NAME, 'row-title'))).get_attribute('innerHTML').split()
		return text[1]


	def post_thumbnail(self, post, problem_id):
		get_to_post = WebDriverWait(post, 20).until(ec.visibility_of_element_located((By.TAG_NAME, 'a'))).get_attribute('href')
		
		self.driver.execute_script('window.open()')
		self.driver.switch_to.window(self.driver.window_handles[1])

		self.driver.get(get_to_post)

		try:
			self.click_on_element_with_id('set-post-thumbnail')
			self.send_keys_to_element_with_id("media-search-input", problem_id)

			try:
				thumbnail = WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, f'//*[@aria-label="{problem_id}"]')))
			except StaleElementReferenceException:
				thumbnail = WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, f'//*[@aria-label="{problem_id}"]')))

			thumbnail.click()
			self.click_on_element_with_xpath('//*[@id="__wp-uploader-id-0"]/div[4]/div/div[2]/button')

		except Exception:
			print("[EROARE]: Problema " + problem_id + " NU are thumbnail.")
			self.click_on_element_with_xpath('//*[@id="__wp-uploader-id-2"]/div[1]/button')

		self.driver.execute_script('window.scrollTo(0, 0)')
		self.click_on_element_with_id('publish')

	def analyze_page(self, page, index):
		self.driver.get(page + str(index))
		
		list_of_posts = WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.ID, 'the-list')))
		list_of_posts = list_of_posts.find_elements_by_tag_name('tr')
		
		for post in list_of_posts:
				if not self.has_thumbnail(post):
					problem_id = self.get_problem_id(post)

					self.post_thumbnail(post, problem_id)
					print(f"[{time.ctime()}]: Am pus thumbnail-ul inapoi problemei cu id-ul {problem_id}!")

					self.driver.close()

					# just to be sure...
					self.driver.switch_to.window(self.driver.window_handles[0])


	def start_reuploading_thumbnails(self):
		page = 'https://tutoriale-pe.net/wp-admin/edit.php?s&cat=706&paged='
		self.driver.get(page)
		
		first_index = 1
		last_index = self.get_num_of_pages() + 1
		
		for index in range(first_index, last_index):
			self.analyze_page(page, index)
			print('----------------------------------------------')
			print(f"[{time.ctime()}]: Am terminat pagina {index}!")
			print('----------------------------------------------')


def main():
	email = input('email:')
	password = input('password:')

	path = convertToOS("path")

	bot = TPN_reupload_thumbnails(email, password, get_driver(path, options))
	bot.login()
	bot.start_reuploading_thumbnails()
	bot.driver.quit()
	
	
if __name__ == '__main__':
	main()