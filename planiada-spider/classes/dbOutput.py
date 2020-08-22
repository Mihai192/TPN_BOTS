from config.constants import db_output_path

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
    sqlQuery = """INSERT INTO objectives (title, url, county_id, city_id, description, short_descr,  meta_title, meta_description, op_hours, p_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    sqlData = (obj.title, obj.url, obj.county_id, obj.city_id, obj.description, obj.short_descr, obj.meta_title, obj.meta_description, obj.opening_hours, obj.p_id)
    sqlConn.execute(sqlQuery, sqlData)

    conn.commit()
    sqlConn.close()

class DBOutput:

    @staticmethod
    def connect():
        conn = None
        try:
            conn = sqlite3.connect(db_output_path)
        except sqlite3.Error as e:
            print(e)
        return conn

    def __init__(self):
        self.dbConn = self.connect()
