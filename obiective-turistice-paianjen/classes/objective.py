from classes.dbOutput import check_output_name, insert_output_obj
from config.functions import build_slug
from main import db_output_conn, b_print

class Objective:
    url = str
    image = str
    city_id = 0
    latitude = 0
    longitude = 0
    description = str
    meta_title = str
    meta_keywords = str
    is_Valid = 0

    def __init__(self, title):
        self.title = title
        self.url = build_slug(title)

    def clone(self, wikiObj):
        self.url = build_slug(wikiObj.title)
        self.city_id = wikiObj.city_id
        self.latitude = wikiObj.latitude
        self.longitude = wikiObj.longitude
        self.meta_title = wikiObj.title
        self.image = ""

    def insertToDB(self):
        if check_output_name(db_output_conn, self.title, self.url) == 0:
            insert_output_obj(db_output_conn, self)
            b_print("[ADAUGAT] " + self.title)
            return True
        else:
            b_print("[EROARE][DUPLICAT]: " + self.title + " exista deja in DB")
            return False

    def checkDB(self):
        return check_output_name(db_output_conn, self.title, self.url)
