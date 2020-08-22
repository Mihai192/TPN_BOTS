from classes.dbCity import check_name
from config.constants import debug
from config.functions import m_print, q_print
from main import db_city_conn

import unidecode as unidecode

class WikiResult:
    title: str
    latitude: float
    longitude: float
    city_id: int
    city_name: str
    obj_title = str
    meta_title: str
    meta_keywords = str

    def __init__(self, obj_soap, obj_title):
        self.soup = obj_soap
        self.obj_title = obj_title
        self.city_name = "null"
        self.city_id = 0

    def setTitle(self):
        self.title = self.soup.find('title').string
        m_print("[wResult]: ObjTitle: " + self.obj_title + " WikiTitle: " + self.title)

    def setGeopoints(self):
        soup_latitude = self.soup.find('a', {"class": "mw-kartographer-maplink"})
        self.latitude = float(soup_latitude['data-lat']) if soup_latitude is not None else float(0)
        self.longitude = float(soup_latitude['data-lat']) if soup_latitude is not None else float(0)
        m_print("[wResult]: ObjTitle: " + self.obj_title + " Lat: " + str(self.longitude) + " Long: " + str(self.latitude))

    def setCityId(self):
        soup_all_tr = self.soup.find("table", {"class": "infocaseta"}).find_all("tr")
        for tr_elem in soup_all_tr:
            soup_tr = tr_elem.find('th', string=["Orașe", "Localitate"])
            if soup_tr is not None:
                self.city_name = tr_elem.find('a').text
                self.city_id = check_name(db_city_conn, unidecode.unidecode(self.city_name))
                m_print("[wResult]: Locatie: " + self.city_name + " [#" + str(self.city_id) + "]")

    def print(self):
        q_print("[OB. Turistic]: " + self.title + " Locatie: " + self.city_name + " [#" + str(self.city_id) + "][Geo: " + str(self.latitude) + " / " + str(self.longitude) + "]")


