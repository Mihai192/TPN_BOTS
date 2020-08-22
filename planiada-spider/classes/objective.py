import os
import urllib
from pathlib import Path

from classes.dbCity import check_name, DBCity
from classes.dbOutput import check_output_name, insert_output_obj, DBOutput
from config.functions import build_slug, b_print, cleanhtml, pln_base

import unidecode
import requests
from bs4 import BeautifulSoup

city_conn = DBCity().connect()
output_conn = DBOutput().connect()

class Objective:
    url = str #
    title = str
    county_id = int #
    city_id = int #
    latitude = float #
    longitude = float #
    description = str #
    short_descr = str #
    meta_title = str #
    meta_description = str #
    opening_hours = str #
    price = int
    p_url = str #
    p_id = int

    def __init__(self, title, county_id, url):
        self.title = title
        self.url = build_slug(title)
        self.county_id = county_id
        self.p_url = url
        self.city_id = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.description = ""
        self.meta_title = title
        self.meta_description = ""
        self.short_descr = ""
        self.opening_hours = ""
        self.price = -1
        self.p_id = 0

    def set_short_ds(self, string):
        self.short_descr = string

    def set_meta_description(self, soup):
        self.meta_description = cleanhtml(str(soup.find("meta", {"name": "description"})['content']))

    def set_description(self, soup):
        self.description = soup.find("div", {"class": "destination-words mb15"}).text.lstrip()

    def set_city_id(self, soup):
        s_breadcrumbs = soup.find_all("li", {"property": "itemListElement", "typeof": "ListItem"})
        s_name = ""
        for s_br in s_breadcrumbs:
            s_name = s_br.find('span').text
        city_string = s_name
        idx_end = city_string.find('jud.')
        idx_beg = city_string.find('.')
        city_name = city_string[idx_beg + 1:idx_end].strip()
        self.city_id = check_name(city_conn, unidecode.unidecode(city_name))

    def set_schedule(self, soup):
        self.opening_hours = cleanhtml(str(soup.find("ul", {"class": "schedule-list"}))).strip()

    def set_p_id(self, soup):
        pid = soup.find('button', {"class": "addPoi2MyPlan"})['data-poi-id']
        self.p_id = pid

    def download_imgs(self, soup):
        Path("images/" + str(self.p_id)).mkdir(parents=True, exist_ok=True)
        images = soup.find_all('img', {"class":"object-fit-cover"})
        img_id = 0
        for s_img in images:
            img_link = s_img['src']
            urllib.request.urlretrieve(pln_base + img_link, "images/" + str(self.p_id) + "/" + str(img_id) + ".jpg")
            img_id = img_id + 1

    def process(self):
        response = requests.get(self.p_url)
        soup = BeautifulSoup(response.text, "html5lib")
        self.set_meta_description(soup)
        self.set_description(soup)
        self.set_city_id(soup)
        self.set_schedule(soup)
        self.set_p_id(soup)
        self.download_imgs(soup)
        self.insertToDB()

    def insertToDB(self):
        insert_output_obj(output_conn, self)
        b_print("[ADAUGAT] " + self.title)
        return True

    def checkDB(self):
        return check_output_name(output_conn, self.title, self.url)
