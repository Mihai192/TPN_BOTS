from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time

path = 'C:\\Drivers\\ChromeDriver\\chromedriver.exe'
options = Options()

users = []
users_file = open("users.txt", 'r+t')

username = input('nume sau email:')
password = input('parola:')
message = 'Am vazut ca te chinui sa rezolvi probleme pe pbinfo.Eu si echipa mea avem un canal cu tutoriale despre programare pe YT,poate vrei sa arunci un ochi;).\nhttps://www.youtube.com/user/MihaiMatraguna'

def set_options(options):
	# options.add_argument('--headless')
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--ignore-ssl-errors')
	options.add_argument('--incognito')

def read_users_file(users):
	for user in users_file:
		users.append(user[:-1])

def get_browser(path, options):
	return webdriver.Chrome(executable_path=path,options=options)

def is_good_link_problem(link):
		if re.search('probleme/[0-9]', str(link.get_attribute('href'))):
			return True
		else:
			return False

def replace_letter_on_problem_link(link):
	return 'https://www.pbinfo.ro/solutii/problema/' + link[len('https://www.pbinfo.ro/probleme/'):]  

def remove_duplicates_links(links):
	return [links[i].get_attribute('href') for i in range(0, len(links)) if i % 2 == 1]

class Pbinfo_Bot:
	def __init__(self, username, password, message, driver):
		self.driver = driver
		self.username = username
		self.message = message
		self.password = password

	def login(self):
		self.driver.get('https://www.pbinfo.ro')
		time.sleep(8)
		username_box = self.driver.find_element_by_id('user')
		password_box = self.driver.find_element_by_id('parola')
		username_box.send_keys(self.username)
		password_box.send_keys(self.password)
		time.sleep(2)
		password_box.submit()

	def sent_user_message(self, user):
		url = 'https://www.pbinfo.ro/?pagina=conversatii&partener=' + user
		self.driver.get(url)
		time.sleep(8)
		text_area = self.driver.find_element_by_id('mesaj')
		text_area.send_keys(self.message)
		text_area.submit()

	def sent_message_to_all_users_on_problem_link(self, problem_link):
		self.driver.get(problem_link)

		problem_details = problem_link[len('https://www.pbinfo.ro/solutii/problema/'):]
		problem_details = problem_details.replace('/', ' si numele ')
		
		time.sleep(8)

		pages = self.driver.find_elements_by_class_name('a-paginare')
		page = pages[-1].get_attribute('href')

		first_page_index = 0
		last_page_index = int(re.findall('\\d+', page)[-1])
		step = 50
		messages_on_this_problem = 0

		last_page_index += step

		while True:
			for index in range(first_page_index, last_page_index, step):
				page_link = problem_link + '?start=' + str(index)
				
				self.driver.get(page_link)
				time.sleep(8)

				Users = self.driver.find_elements_by_tag_name('a')
				Users = [user.get_attribute('href') for user in Users if re.search('profil', str(user.get_attribute('href')))]
			
				for user in Users:
					if user[29:] not in users:
						try:
							self.sent_user_message(user[29:])
							print('[' + time.ctime() + ']: ' + 'Am trimis mesaj user-ului ' + user[29:])
							messages_on_this_problem += 1
						except:
							print('[' + time.ctime() + ']: ' + 'Nu am putut trimite mesaj user-ului ' + user[29:] + '(probabil are contul pe privat...)')
						                                                                                                                                        
						users.append(user[29:])
						users_file.write(user[29:] + '\n')
						time.sleep(8)

			print('[' + time.ctime() + ']: ' + 'Am trimis ' + str(messages_on_this_problem) + ' de mesaje la problema cu id-ul ' + problem_details)
		
									
	def start_sending_messages(self):
		problems_list = 'https://www.pbinfo.ro/?pagina=probleme-lista&clasa=-1&start='
		
		first_page_index = 0
		last_page_index = 2920
		step = 10

		last_page_index += step
		for index in range(first_page_index, last_page_index, step):
			problem_page = problems_list + str(index)
			
			self.driver.get(problem_page)
			time.sleep(8)

			problems_link = list(filter(is_good_link_problem, self.driver.find_elements_by_tag_name('a')))
			
			problems_link = remove_duplicates_links(problems_link)

			problems_link = map(replace_letter_on_problem_link, problems_link)

			for problem_link in problems_link:
				self.sent_message_to_all_users_on_problem_link(problem_link)
				time.sleep(8)
			
			print('[' + time.ctime() + ']: ' + 'Am terminat pagina ' + str(index / step + 1) + '!')			

	def __del__(self):
		self.driver.close()


read_users_file(users)

set_options(options)		
bot = Pbinfo_Bot(username, password, message, get_browser(path, options))
bot.login()
bot.start_sending_messages()

users_file.close()
