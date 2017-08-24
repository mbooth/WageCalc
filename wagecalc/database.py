import sqlite3
from PyQt5 import QtSql

class Db(QtSql.QSqlDatabase):
    def __init__(self, dbname):
        # try:
        # QtSql.QSqlDatabase.__init__(self)
        QtSql.QSqlDatabase.addDatabase("QSQLITE")
        # self.cur=self.cursor()
        self.setDatabaseName(dbname)
        # print("Database connected")
        # except:
        # print("Could not connect to the database")
        self.open()

    # def insert(self, query, params):
    #     self.cur.execute(query, params)
    #     self.commit()
    #
    # def query(self, query, params):
    #     return self.cur.execute(query, params)
    #

def close_db(self):
    try:
        self.db.close()
        print("Database closed successfully")
    except:
        print("Could not close database")
    return