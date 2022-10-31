'''Crear base de datos para almacenar blobs con permisos de lectura y escritura'''
import sqlite3
import os
import sys

class BlobDB():

    def __init__(self, db_path):
        '''Inicializar base de datos'''
        self.db_path = db_path
        if not os.path.isfile(db_path):
            BlobDB._create_db()

    def _create_db(self):
        '''Crear base de datos'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE blobs (id INTEGER PRIMARY KEY, string path)''')
        c.execute('''CREATE TABLE permissions (blob_id INTEGER, user_id INTEGER, readable_by INTEGER, writable_by INTEGER)''')
        conn.commit()
        conn.close()

    def add_blob(self, path, user):
        '''Agregar blob a la base de datos'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO blobs (path) VALUES (?)''', (path,))
        conn.commit()
        c.execute('''INSERT INTO permissions (blob_id, user_id, readable_by, writable_by) VALUES (?, ?, ?, ?)''', (c.lastrowid, user, 1, 1))
        conn.close()

    def remove_blob(self, blob_id):
        '''Eliminar blob de la base de datos'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''DELETE FROM blobs WHERE id=?''', (blob_id,))
        conn.commit()
        c.execute('''DELETE FROM permissions WHERE blob_id=? ''', (blob_id,))
        conn.close()

    def get_blob(self, blob_id):
        '''Obtener blob de la base de datos'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT path FROM blobs WHERE id=?''', (blob_id,))
        path = c.fetchone()
        c.execute('''SELECT user_id FROM permissions WHERE blob_id=? AND readable_by=1''', (blob_id,))
        readable_by = c.fetchall()
        c.execute('''SELECT user_id FROM permissions WHERE blob_id=? AND writable_by=1''', (blob_id,))
        writable_by = c.fetchall()
        conn.close()
        return path, readable_by, writable_by

    def add_write_permission(self, blob_id, user):
        '''Agregar permiso de escritura a un blob'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''UPDATE permissions SET writable_by=1 WHERE blob_id=? AND user_id=?''', (blob_id, user))
        conn.commit()
        conn.close()

    def revoke_write_permission(self, blob_id, user):
        '''Revocar permiso de escritura a un blob'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''UPDATE permissions SET writable_by=0 WHERE blob_id=? AND user_id=?''', (blob_id, user))
        conn.commit()
        conn.close()

    def add_read_permission(self, blob_id, user):
        '''Agregar permiso de lectura a un blob'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''UPDATE permissions SET readable_by=1 WHERE blob_id=? AND user_id=?''', (blob_id, user))
        conn.commit()
        conn.close()

    def revoke_read_permission(self, blob_id, user):
        '''Revocar permiso de lectura a un blob'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''UPDATE permissions SET readable_by=0 WHERE blob_id=? AND user_id=?''', (blob_id, user))
        conn.commit()
        conn.close()
    
    def have_read_permission(self, blob_id, user):
        '''Verificar si un usuario tiene permiso de lectura'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT readable_by FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user))
        permission = c.fetchone()
        conn.close()
        return permission
    
    def have_write_permission(self, blob_id, user):
        '''Verificar si un usuario tiene permiso de escritura'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT writable_by FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user))
        permission = c.fetchone()
        conn.close()
        return permission