from config.constants import file_name_dbResult

import sqlite3


def check_output_name(conn, string, url):
    c = conn.cursor()
    c.execute("SELECT id FROM objectives WHERE title LIKE ?", ('%'+string+'%', ))
    exists = c.fetchall()
    if not exists:
        c.execute("SELECT id FROM objectives WHERE url LIKE ?", ('%' + url + '%',))
        exists = c.fetchall()
        if not exists:
            return 0
        else:
            return 1
    else:
        return 1

def insert_output_obj(conn, obj):
    sqlConn = conn.cursor()
    sqlQuery = """INSERT INTO objectives (title, url, image, city_id, latitude, longitude, meta_title) VALUES (?, ?, ?, ?, ?, ?, ?);"""
    sqlData = (obj.title, obj.url, obj.image, obj.city_id, obj.latitude, obj.longitude, obj.meta_title)
    sqlConn.execute(sqlQuery, sqlData)

    conn.commit()
    sqlConn.close()

class DBOutput:

    @staticmethod
    def connect():
        conn = None
        try:
            conn = sqlite3.connect(file_name_dbResult)
        except sqlite3.Error as e:
            print(e)
        return conn

    def __init__(self):
        self.dbConn = self.connect()
