# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 16:17:42 2020

@author: Jill Wright 

This program takes information  from an API program called Financial Prep
and commits it to a SQL database. The information is from ticker symbol and includes
Industry,CEO, and company description. Another segment is populated with information
articles also pulled from the API that can be reviewed by the user.

"""

import sqlite3

try:
#     Create the StockINFO database then the company table  
    conn = sqlite3.connect('STOCKINFORM')

    cursor = conn.cursor()
    print("Connected")
    comtable_sql='''
                    CREATE TABLE IF NOT EXISTS
                        COMPANY(
                            pkid INTEGER,
                            symbol TEXT PRIMARY KEY,
                            Company INTEGER NOT NULL,
                            CEO TEXT NOT NULL,
                            DESC TEXT,
                            Industry INTEGER NOT NULL
                        )
        
                '''
    cursor.execute(comtable_sql)
    conn.commit()
    print("Created Company table")
    
    
    
except sqlite3.Error as error:
    print("Error")
    print(error)
# Close Resource
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    


# In[ ]:


def close_DB_resources(dbconn, cursor):
    try:
        if dbconn:
            dbconn.close()
        if cursor:
            cursor.close()
        print("closed resources")
    except sqlite3.Error as err:
        ("Error closing resources")


# In[ ]:


import sqlite3
# Utility for handling DB errors
def handle_DB_error(dbconn, cursor):
    if dbconn:
        try:
            dbconn.rollback()
            print("Rolled back transation")
        except sqlite3.Error as error:
            print("Error rolling back transaction")
            close_DB_resources(dbconn, cursor)
            dbconn = None
            return dbconn
            


# In[ ]:


# utility DB connection and cursor function to return our access objects
def connect_SQLite():
    try:
        dbconn = sqlite3.connect('STOCKINFORM')
        cursor = dbconn.cursor()
        print("Connected to STOCK DATABASE")
    except sqlite3.Error as error:
        print("Error opening database")
        dbconn = handle_DB_error(dbconn, cursor)
    return dbconn, cursor
        
        


# In[ ]:


import csv
# SQL setup for insert of company information
pkid = 101
company_insert = '''INSERT INTO COMPANY (pkid, symbol, Company, CEO, Industry)
                   VALUES (?,?,?,?,?);
                '''
# retrieve my connection and cursor for use in all my inserts
dbconn, cursor = connect_SQLite()
# Iterate over our CSV file of appointments, convert the missedappt to 0/1
with open('companyinfo.csv') as file:
    print('reading comp csv')
    compinfo = csv.DictReader(file)
    print(compinfo)
    for comp in compinfo:
        # get rowid from generator
        pkid += 1
        record = (pkid,comp['symbol'],comp['Company'], comp['CEO'],comp['Industry'])
        print("inserting records: ", end='')
        print(record)
        cursor.execute(company_insert, record)
        dbconn.commit()



# In[ ]:


# Verify that we've got data

select_sql = '''
                SELECT *
                    FROM COMPANY;
            '''
dbconn, cursor = connect_SQLite()
cursor.execute(select_sql)
recs = cursor.fetchall()
for r in recs:
    print(r)

#close_DB_resources(dbconn, cursor)

# In[22]:


#Create our table for student registration data

STK_table_sql= '''CREATE TABLE IF NOT EXISTS stock(
                    pkid INTEGER PRIMARY KEY,
                    symbol TEXT,
                    text TEXT,
                    urlinfo TEXT );
                '''
dbconn, cursor = connect_SQLite()
cursor.execute(STK_table_sql)
dbconn.commit()
print('Create stock table')


# In[24]:

import csv
# Complete insert of news url info
pkid = 101
stock_insert = '''INSERT INTO stock (pkid,symbol, text, urlinfo)
                    VALUES (?,?,?,?);
                '''
# retrieve my connection and cursor for use in all my inserts
dbconn, cursor = connect_SQLite()
# Iterate over our CSV file for the url for the recent news on the ticker symbol 
with open('stockinfo.csv') as file:
    stockinfo = csv.DictReader(file)
    for stock in stockinfo:
        # get rowid from generator
        pkid += 1
        record = (pkid, stock['symbol'], stock['text'], stock['urlinfo'])
        print("inserting records: ", end='')
        print(record)
        cursor.execute(stock_insert, record)
        dbconn.commit()
#        close_DB_resources(dbconn, cursor)

select_sql = '''
                SELECT *
                    FROM stock;
            '''
dbconn, cursor = connect_SQLite()
cursor.execute(select_sql)
recs = cursor.fetchall()
for r in recs:
    print(r)
close_DB_resources(dbconn, cursor)

class _TimesCalled: 
    def __init__(self): 
        self._called = 0 
    def __add__(self, other): 
        self._called = self._called + other 
        return self._called
    def __str__(self):
        return str(self._called)
times_called = _TimesCalled() 
def increment(): 
    return times_called + 1 


