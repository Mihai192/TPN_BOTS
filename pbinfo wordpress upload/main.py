'''
	Add db functionality
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import StaleElementReferenceException

import os
import platform
import time 
import re

pbinfo_url = 'https://www.pbinfo.ro/'
login_page = 'https://tutoriale-pe.net/wp-login.php'
options = Options()

def set_options(options):
	options.add_argument('no-sandbox')
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--ignore-ssl-errors')
	options.add_argument('--disable-gpu')
	options.add_argument('--incognito')
	options.add_argument('--start-maximized')

def get_driver(path, options):
	return webdriver.Chrome(executable_path=path, options=options)

class TPN_post_problems_bot:
	def __init__(self, email, password, driver):
		self.email = email
		self.password = password
		self.driver = driver

	def problem_title_TPN(self, id):
		self.driver.get(pbinfo_url)
		
		search_box = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.ID, 'search_box')))
		search_box.send_keys('#' + str(id))
		search_box.submit()

		h1 = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, 'text-primary')))
		h1 = h1.text.replace(' ', '-')
		h1 = h1.split('-')

		return 'Problema ' + h1[0] + ' - ' + h1[1] + ' - Rezolvari PBInfo'
	
	def remove_ad(self, file):
		first_index = file.find('<br>')
		last_index = file.rfind('</script>')

		if last_index != -1:
			return file[:first_index] + file[last_index + len('</script>'):]
		else:
			return file

	def replace_includes(self, file):
		# &lt; <
		# &gt; > 

		find = re.search('#include <\\w+>', file)
		change = '#include &lt;bits/stdc++.h&gt;'

		while find:
			include = find[0]
			
			file = file.replace(include, change)
			find = re.search('#include <\\w+>', file)
			change = ''

		return file
	
	def check_boxes(self):
		check_box_pbinfo = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, "in-category-706")))
		check_box_cpp = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, "in-category-8")))
		check_box_tutoriale = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, "in-category-3")))
		
		check_box_pbinfo.click()
		check_box_cpp.click()
		check_box_tutoriale.click()


	def send_keys_to_element_with_id(self, id, keys):
		element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.ID, id)))
		time.sleep(2)
		element.send_keys(keys)

	def click_on_element_with_id(self, id):
		element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, id)))
		time.sleep(2)
		element.click()

	def click_on_element_with_xpath(self, xpath):
		element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
		time.sleep(2)
		element.click()

	def post_problem(self, problem_id, post_title, post_problems):
		self.send_keys_to_element_with_id("title", post_title)
		self.click_on_element_with_id("content-html")

		text_area = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="content"]')))
		
		post_problems = post_problems.split('\n') 
		newline = False

		for line in post_problems:
			for character in line:
				if character == '\t':
					text_area.send_keys(Keys.TAB)
				else:
					text_area.send_keys(character)

			if line.find('<pre class="EnlighterJSRAW" data-enlighter-language="cpp">') != -1:
				newline = True

			if newline:
				text_area.send_keys(Keys.RETURN)
		
		self.check_boxes()
		self.click_on_element_with_id('set-post-thumbnail')
		self.send_keys_to_element_with_id("media-search-input", f"/{problem_id}.png")
				
		# dummy value
		thumbnail_list = 0
		
		try:
			thumbnail = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, f'//*[@aria-label="#{problem_id}"]')))
		except StaleElementReferenceException:
			thumbnail = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, f'//*[@aria-label="#{problem_id}"]')))

		
		thumbnail.click()
		self.click_on_element_with_xpath('//*[@id="__wp-uploader-id-0"]/div[4]/div/div[2]/button')
		self.driver.execute_script('window.scrollTo(0, 0)')
		self.click_on_element_with_id('publish')
		
		
	def login(self):
		self.driver.get(login_page)
		self.send_keys_to_element_with_id('user_login', self.email)
		self.send_keys_to_element_with_id('user_pass', self.password)
		self.click_on_element_with_id('wp-submit')

	def start_posting_problems(self):
		problem_file = '.\\Rezolvari PBInfo' #Windows

		# problem_file = 'Rezolvari PBInfo'  # Linux

		files = os.listdir(problem_file)
		
		for file in files:
			open_file = open('{}\\{}'.format(problem_file, file), 'rt', encoding='UTF-8') # Windows

			# open_file = open('{}/{}'.format(problem_file, file), 'rt', encoding='UTF-8') # Linux

			problem_str = str(open_file.read())

			problem_title = self.problem_title_TPN('{}'.format(file[:-4]))

			open_file.close()

			self.driver.get('https://tutoriale-pe.net/wp-admin/post-new.php')

			problem_str = self.remove_ad(problem_str)
			problem_str = self.replace_includes(problem_str)
			

			try:
				self.post_problem(file[:-4], problem_title, problem_str)
			except Exception:
				return
			
			print(f"[{time.ctime()}]: Am postat problema cu id-ul {'#' + file[:-4]}!")
			

def main():
	set_options(options)

	email = input('email:')
	password = input('password:')

	# modify here path according to your os
	path = f'.\\chromedriver.exe' #Windows
	# path = "./chromedriver" #Linux

	problem_path = '.\\Rezolvari PBInfo' #Windows
	# problem_path = '/Rezolvari PBInfo' #Linux

	bot = TPN_post_problems_bot(email, password, webdriver.Chrome(executable_path=path, options=options))
	bot.login()
	bot.start_posting_problems()
	bot.driver.quit()

if __name__ == '__main__':
	main()
