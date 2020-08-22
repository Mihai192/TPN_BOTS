from classes.objective import Objective
from config.constants import pln_county_url, counties
from config.functions import b_print, c_print

from bs4 import BeautifulSoup
import requests

class pCounty:
    id: int
    pId: int
    url: str
    title: str

    def __init__(self, id, url):
        self.url = url
        self.id = id

    def setTitle(self, soup):
        s_breadcrumbs = soup.find_all("li", {"property" : "itemListElement", "typeof" : "ListItem"})
        s_name = ""
        for s_br in s_breadcrumbs:
            s_name = s_br.find('span').text
        self.title = s_name

    def processPage(self, page):
        c_added = 0
        response = requests.get(pln_county_url + str(self.url) + "?&_page=" + str(page))
        soup = BeautifulSoup(response.text, "html5lib")
        self.setTitle(soup)

        cObjectives = soup.find_all("div", {"class": "activity-item"})

        for cObj in cObjectives:
            cTitle = cObj.find("h3").find("a").text.strip()
            cURL = cObj.find("h3").find("a")['href']
            cShortDsc = cObj.find("p", {"class": "mb20 shortdesciption _3lines"}).text.lstrip()

            objective = Objective(cTitle, self.id, cURL)
            if objective.checkDB() == 0:
                objective.set_short_ds(cShortDsc)
                objective.process()
                c_added = c_added + 1
        return c_added

    def process(self):
        t_added = 0
        c_page = 1
        c_added = self.processPage(c_page)
        while c_added >= 1:
            t_added = t_added + c_added
            c_page = c_page + 1
            c_added = self.processPage(c_page)

        c_print("[# " + str(self.id) + "/" + str(len(counties)) + "] Am gasit " + str(t_added) + " obiective")