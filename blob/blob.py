'''Crear base de datos para almacenar blobs'''
import sqlite3
import os
import sys

def create_db():
    '''Crear base de datos'''
    conn = sqlite3.connect('blob.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE blob
                 (id integer primary key, blob blob)''')
    conn.commit()
    conn.close()
    


