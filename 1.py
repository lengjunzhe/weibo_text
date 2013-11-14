#coding:utf-8

import sqlite3,os

con = sqlite3.connect('weibo_text.db')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#print (cursor.fetchall())

cursor.execute("PRAGMA table_info(weibo_text_g_u)")
print cursor.fetchall()

