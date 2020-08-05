'''
  TODO:Add db functionality
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import StaleElementReferenceException

import sqlite3
from sqlite3 import Error

import pyperclip
import os
import platform
import time 
import re

pbinfo_url = 'https://www.pbinfo.ro/'
login_page = 'https://tutoriale-pe.net/wp-login.php'
options = Options()

def sql_create_connection(db_file):
	return sqlite3.connect(db_file)
	 
def sql_create_table(db_file, table):
	c = db_file.cursor()
	c.execute(table)

def sql_insert(db_file, id):
	sql = f"""INSERT INTO problems(ID) VALUES('{id}')"""
	
	cur = db_file.cursor()
	cur.execute(sql)

	db_file.commit()
	

def sql_check_id(db_file, id):
	sql = f"""SELECT EXISTS (SELECT 1 FROM problems WHERE ID='{id}');"""

	cur = db_file.cursor()
	check = cur.execute(sql)

	return check

def change_string_at_index(string, index, string_to_change):
	return string[:index] + string_to_change + string[index + 1:]

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
	def __init__(self, email, password, driver, db):
		self.email = email
		self.password = password
		self.driver = driver
		self.db = db
	
	def remove_ad(self, file):
		index = file.find('</div>')

		# remove 1st ad
		if index != -1:
			file = file[index + len('</div>'):]

		first_index = file.find('<br>')
		second_index = file.rfind('</script>')

		# remove 2st ad
		if first_index != -1:
			file = file[:first_index] + file[second_index + len('</script>'):]

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

	def replace_less_then(self, file):
		# &lt; <
		code_tag = '<pre class="EnlighterJSRAW" data-enlighter-language="cpp">'
		index = int(file.find(code_tag))
		str_len = len(code_tag)
		
		find_index = file.find('<', index + str_len)

		while find_index != -1:
			file = change_string_at_index(file, find_index, '&lt;')
			find_index = file.find('<', find_index)			

		find_index = file.rfind('&lt;')
		file = file[:find_index] + '<' + file[find_index + 4:]

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
		pyperclip.copy(keys)
		element.send_keys(Keys.CONTROL, 'v')
		return element

	def click_on_element_with_id(self, id):
		element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, id)))
		time.sleep(2)
		element.click()

	def click_on_element_with_xpath(self, xpath):
		element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
		time.sleep(2)
		element.click()

	def get_solution(self, file):
		return file[file.find('<pre class="EnlighterJSRAW" data-enlighter-language="cpp">'):]

	# problem_id = '#{int}'
	def get_statement(self, problem_id):
		self.driver.get(pbinfo_url)

		search_box = self.send_keys_to_element_with_id('search_box', problem_id)
		search_box.submit()

		statement = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.TAG_NAME, "article")))
		
		h1 = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, 'text-primary')))
		h1 = h1.text.replace(' ', '-')
		h1 = h1.split('-')

		h1 = 'Problema ' + h1[0] + ' - ' + h1[1] + ' - Rezolvari PBInfo'

		return statement.get_attribute('innerHTML'), h1

	def post_problem(self, problem_id, post_title, post_problems):
		self.driver.get('https://tutoriale-pe.net/wp-admin/post-new.php')

		self.send_keys_to_element_with_id("title", post_title)
		self.click_on_element_with_id("content-html")

		text_area = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="content"]')))

		pyperclip.copy(post_problems)
		text_area.send_keys(Keys.CONTROL, 'v')

		self.check_boxes()
		try:
			self.click_on_element_with_id('set-post-thumbnail')
			self.send_keys_to_element_with_id("media-search-input", f"/{problem_id}.png")

			try:
				thumbnail = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, f'//*[@aria-label="#{problem_id}"]')))
			except StaleElementReferenceException:
				thumbnail = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, f'//*[@aria-label="#{problem_id}"]')))


			thumbnail.click()
			self.click_on_element_with_xpath('//*[@id="__wp-uploader-id-0"]/div[4]/div/div[2]/button')
		except Exception:
			print("[EROARE]: Problema #" + problem_id + " NU are thumbnail.")

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
			if not sql_check_id(self.db, '#' + file[:-4]):
				open_file = open('{}\\{}'.format(problem_file, file), 'rt', encoding='UTF-8') # Windows
				# open_file = open('{}/{}'.format(problem_file, file), 'rt', encoding='UTF-8') # Linux

				problem_str = str(open_file.read())

				open_file.close()
				
				problem_statement, post_title = self.get_statement('#' + file[:-4])
				problem_solution = self.get_solution(problem_str)

				problem = problem_statement + problem_solution


				problem = self.remove_ad(problem)

				problem = self.replace_includes(problem)

				problem = self.replace_less_then(problem)

				
				try:
					self.post_problem(file[:-4], post_title, problem)
				except Exception:
					return
				
				print(f"[{time.ctime()}]: Am postat problema cu id-ul {'#' + file[:-4]}!")

				sql_insert(self.db, file[:-4])

	def __del__(self):
		self.driver.close()
		self.db.close()
		
def main():
	set_options(options)
	
	db = sql_create_connection('posted_problems.sqlite')
	sql_create_table(db, """CREATE TABLE IF NOT EXISTS problems (ID TEXT NOT NULL);""")

	email = input('email:')
	password = input('password:')

	path = '.\\chromedriver.exe' #Windows
	# path = "./chromedriver" #Linux

	problem_path = '.\\Rezolvari PBInfo' #Windows
	# problem_path = '/Rezolvari PBInfo' #Linux
	
	bot = TPN_post_problems_bot(email, password, webdriver.Chrome(executable_path=path, options=options), db)
	bot.login()
	bot.start_posting_problems()
	

if __name__ == '__main__':
	main()
