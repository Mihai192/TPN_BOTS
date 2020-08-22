from config.constants import file_name_dbCity

import sqlite3


def check_name(conn, string):
    c = conn.cursor()
    c.execute("SELECT id FROM cities WHERE name LIKE ?", ('%'+string+'%', ))
    exists = c.fetchall()
    if not exists:
        return 0
    else:
        return int(exists[0][0])

class DBCity:

    @staticmethod
    def connect():
        conn = None
        try:
            conn = sqlite3.connect(file_name_dbCity)
        except sqlite3.Error as e:
            print(e)
        return conn

    def __init__(self):
        self.dbConn = self.connect()
