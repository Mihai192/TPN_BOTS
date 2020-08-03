import requests
import bs4
from selenium import webdriver
import time

path = 'C:\\Drivers\\ChromeDriver\\chromedriver.exe'
driver = webdriver.Chrome(path)

message_file = open("message.txt", 'rt')
users_file = open("users.txt", 'r+t')

message = ''
first_solution_page = 0
last_solution_page = 5100
jump = 50
count_new_users = 0

username = message_file.readline()
password = message_file.readline()

message_time_between = int(message_file.readline())

for m in message_file:
    message = message + m

users = []

for user in users_file:
    users.append(user[:-1])

print('-------------------------------------------------------------')
print('Script developed by nonam3')
print('RECOMANDARE:Pastrati intervalul de timp intre mesaje la 60 secunde minim!')
print('-------------------------------------------------------------')

def login():
    driver.get('https://www.pbinfo.ro/')
    username_box = driver.find_element_by_id('user')
    password_box = driver.find_element_by_id('parola')
    username_box.send_keys(username)
    password_box.send_keys(password)
    password_box.submit()


def sent_message(url, message):
    driver.get(url)
    time.sleep(message_time_between)
    text_area = driver.find_element_by_id('mesaj')
    text_area.send_keys(message)
    text_area.submit()


login()

for index in range(first_solution_page, last_solution_page, jump):
    message_per_page = 0
    # get page source code
    page = requests.get("https://www.pbinfo.ro/solutii?start=" + str(index))

    time.sleep(5)
    # parse the source code

    reformat = bs4.BeautifulSoup(page.content, 'html.parser')

    # find all links
    links = reformat.find_all('a')

    # find users links
    profiles = []

    links = list(links)

    for link in links:
        save = link.get('href')
        if type(save) is str and save.find('profil') != -1:
            profiles.append(save)

    # get users name and sent message

    url = 'https://www.pbinfo.ro/?pagina=conversatii&partener='

    for profile in profiles:
        if profile[8:] not in users:
            count_new_users = count_new_users + 1

            try:
                sent_message(url + profile[8:], message)
                print('[' + time.ctime() + ']: ' + 'Am trimis mesaj user-ului ' + profile[8:])
                message_per_page = message_per_page + 1
            except:
                print('[' + time.ctime() + ']: ' + 'Nu am putut trimite mesaj user-ului ' + profile[
                                                                                            8:] + '(probabil are '
                                                                                                  'contul pe '
                                                                                                  'privat...)')
            users.append(profile[8:])
            users_file.write(profile[8:] + '\n')

    print('[' + time.ctime() + ']: ' + 'Am terminat pagina ' + str(index // 50 + 1) + ' si am trimis ' + str(message_per_page) + '  mesaje!')



driver.quit()
message_file.close()
users_file.close()

