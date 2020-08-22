import unidecode as unidecode

from classes.dbCity import check_name
from config.functions import m_print

from main import db_city_conn

class WikiResult:
    title: ""
    latitude: float
    longitude: float
    city_id: int
    obj_title = ""
    meta_title: ""
    meta_keywords = ""

    def __init__(self, obj_soap, obj_title):
        self.soup = obj_soap
        self.obj_title = obj_title

    def setTitle(self):
        self.title = self.soup.find('title').string
        m_print("[wResult]: ObjTitle: " + self.obj_title + " WikiTitle: " + self.title)

    def setGeopoints(self):
        soup_latitude = self.soup.find('a', {"class": "mw-kartographer-maplink"})
        self.latitude = float(soup_latitude['data-lat']) if soup_latitude is not None else float(0)
        self.longitude = float(soup_latitude['data-lat']) if soup_latitude is not None else float(0)
        m_print("[wResult]: ObjTitle: " + self.obj_title + " Lat: " + str(self.longitude) + " Long: " + str(self.latitude))

    def setCityId(self):
        #soup_city = self.soup.find("table", {"class": "infocaseta"}).find_all("tr").find("th", string="Localitate")
        soup_all_tr = self.soup.find("table", {"class": "infocaseta"}).find_all("tr")
        for tr_elem in soup_all_tr:
            soup_tr = tr_elem.find('th', string=["Orașe", "Localitate"])
            if soup_tr is not None:
                wiki_city = tr_elem.find('a').text
                self.city_id = check_name(db_city_conn, unidecode.unidecode(wiki_city))
                m_print("[wResult]: Locatie: " + wiki_city + " [#" + str(self.city_id) + "#]")
        #soup.find("table", {"class": "tablehead"}).find_all("tr", {"class": ["oddrow", "evenrow"]})



