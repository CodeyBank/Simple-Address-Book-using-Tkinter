import sqlite3
#from addressbook_frontend import *
# This class handles the database methods for the registration page
#from GUI.Addressbook.addressbook_frontend import f_name, l_name, city, state, addr, zipcode
#from tkinter import *

class db:
    def __init__(self, tablename):
        self.conn = sqlite3.connect(tablename + '.db')
        #self.tablename = tablename
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS contacts (
        id integer primary key,
        first_name text,
        last_name text,
        address text,
        city text,
        state text,
        zipcode int)
        """)
        self.conn.commit()


    def insert(self, fname, lname, address, cty, states, zipcd):
        self.c.execute("INSERT INTO contacts VALUES(NULL,?,?,?,?,?,?)", (fname, lname, address, cty, states, zipcd))
        self.conn.commit()
        # Clear the entries

    def __del__(self):
        self.conn.close()