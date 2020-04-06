# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 18:26:30 2020

@author: Bengi
"""

import sqlite3
from sqlite3 import Error

   
def sql_connection():
 
    try:
      conn = sqlite3.connect('db.sqlite')
      cursor = conn.cursor()
    
    except Error:
        print(Error)

    
    return cursor,conn


def retrieveUsers():
	con = sqlite3.connect("db.sqlite")
	cur = con.cursor()
	cur.execute("SELECT user_id from triplets_file ")
	users = cur.fetchall()
	con.close()
	return users