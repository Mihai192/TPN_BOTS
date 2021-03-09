import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time

path = './chromedriver'
options = Options()

username = "plaformadeinfo"
password = "plaformadeinfo1"
message1 = 'Salutare, nu stiu daca ai aflat, dar s-a deschis cea mai interactiva platforma de unde poti invata informatica: https://platforma-de.info/ - te asteptam sa iti faci cont.'
message2 = 'De asemenea, arunca un ochi si pe canalul de YouTube: https://bit.ly/youtubeTPN - explicam algoritmi si structuri de date, rezolvam subiecte de Bacalaureat si multe altele!'

def sql_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn

def sql_insertUser(conn, paramUser):
    c = conn.cursor()
    c.execute("INSERT INTO users(username) VALUES(?)", (paramUser,))
    conn.commit()
    return c.lastrowid

def sql_checkUser(conn, paramUser):
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username= ?", (paramUser,))
    exists = c.fetchall()
    if not exists:
        return False
    else:
        return True

def set_options(options):
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')


def get_browser(path, options):
    return webdriver.Chrome(executable_path=path, options=options)


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
    def __init__(self, username, password, message1, message2, driver):
        self.driver = driver
        self.username = username
        self.message1 = message1
        self.message2 = message2
        self.password = password

    def login(self):
        self.driver.get('https://www.pbinfo.ro')
        time.sleep(1)
        username_box = self.driver.find_element_by_id('user')
        password_box = self.driver.find_element_by_id('parola')
        username_box.send_keys(self.username)
        password_box.send_keys(self.password)
        time.sleep(1)
        password_box.submit()
        time.sleep(5)

    def sent_user_message(self, user):
        url = 'https://www.pbinfo.ro/?pagina=conversatii&partener=' + user
        self.driver.get(url)
        time.sleep(1)
        text_area = self.driver.find_element_by_id('mesaj')
        text_area.send_keys(self.message1)
        text_area.submit()
        time.sleep(1)
        text_area = self.driver.find_element_by_id('mesaj')
        text_area.send_keys(self.message2)
        text_area.submit()

    def sent_message_to_all_users_on_problem_link(self, problem_link):
        self.driver.get(problem_link)

        problem_details = problem_link[len('https://www.pbinfo.ro/solutii/problema/'):]
        problem_details = problem_details.replace('/', ' si numele ')

        time.sleep(1)

        pages = self.driver.find_elements_by_class_name('a-paginare')
        page = pages[-1].get_attribute('href')

        first_page_index = 0
        last_page_index = int(re.findall('\\d+', page)[-1])
        step = 50
        messages_on_this_problem = 0

        last_page_index += step
        for index in range(first_page_index, last_page_index, step):
            page_link = problem_link + '?start=' + str(index)

            self.driver.get(page_link)
            time.sleep(1)

            Users = self.driver.find_elements_by_tag_name('a')
            Users = [user.get_attribute('href') for user in Users if
                     re.search('profil', str(user.get_attribute('href')))]

            for user in Users:
                strUsername = user[29:]
                if sql_checkUser(conn, strUsername) is False:
                    try:
                        self.sent_user_message(user[29:])
                        print('[' + time.ctime() + ']: ' + 'Am trimis mesaj user-ului ' + user[29:])
                        messages_on_this_problem += 1
                    except:
                        print('[' + time.ctime() + ']: ' + 'Nu am putut trimite mesaj user-ului ' + user[
                                                                                                    29:] + '(probabil are contul pe privat...)')

                    sql_insertUser(conn, strUsername)
                    time.sleep(1)

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
            time.sleep(1)

            problems_link = list(filter(is_good_link_problem, self.driver.find_elements_by_tag_name('a')))

            problems_link = remove_duplicates_links(problems_link)

            problems_link = map(replace_letter_on_problem_link, problems_link)

            for problem_link in problems_link:
                self.sent_message_to_all_users_on_problem_link(problem_link)
                time.sleep(1)

            print('[' + time.ctime() + ']: ' + 'Am terminat pagina ' + str(index / step + 1) + '!')

    def __del__(self):
        self.driver.close()


#sqlFile = r"C:\sqlite\db\pythonsqlite.db"
sqlFile = r"./dbpbinfo.sqlite"
conn = sql_connect(sqlFile)

set_options(options)
bot = Pbinfo_Bot(username, password, message1, message2, get_browser(path, options))
bot.login()
bot.start_sending_messages()