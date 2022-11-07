'''Crear base de datos para almacenar blobs con permisos de lectura y escritura'''

import sqlite3
import os
import uuid

class BlobDB():

    def __init__(self, db_path, storage_path):
        '''Inicializar base de datos'''
        self.db_path = db_path
        self.storage_path = storage_path
        if not os.path.exists(self.db_path):
            self._create_db()
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def _create_db(self):
        '''Crear base de datos'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        '''Si no existe la base de datos, crearla'''
        c.execute('''CREATE TABLE blobs (id STRING PRIMARY KEY, path TEXT)''')
        c.execute('''CREATE TABLE permissions (id INTEGER PRIMARY KEY, blob_id STRING, user_id INTEGER, readable_by INTEGER, writable_by INTEGER)''')
        conn.commit()
        conn.close()


    def add_blob(self,blob_id,local_filename, user):

        '''Agregar blob a la base de datos'''
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''INSERT INTO blobs (id, path) VALUES (?,?)''', (blob_id, local_filename,))
            conn.commit()
            c.execute('''INSERT INTO permissions (blob_id, user_id, readable_by, writable_by) VALUES (?, ?, ?, ?)''', (blob_id, user, 1, 1))
            conn.commit()
            conn.close()
            
            return blob_id
        except Exception as e:
            print(e)
            return None

    
    def remove_blob(self, blob_id):
        '''Eliminar blob de la base de datos'''
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''DELETE FROM blobs WHERE id=?''', (blob_id,))
            conn.commit()
            c.execute('''DELETE FROM permissions WHERE blob_id=? ''', (blob_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.exceptions as e:
            print(e)
            return False

    def get_blob(self, blob_id):
        '''Obtener blob de la base de datos'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT path FROM blobs WHERE id=?''', (blob_id,))
        path = c.fetchone()
        conn.close()
        if path == None:
            return None
        else:
            return path[0]

    def update_blob_path(self, blob_id, blob):
        try:
            '''Actualizar blob'''
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''UPDATE blobs SET path=? WHERE id=?''', (blob, blob_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def add_write_permission(self, blob_id, user):
        '''Agregar permiso de escritura a un blob para un usuario y si no existe, crearlo'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT * FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user))
        permission = c.fetchone()
        if permission == None:
            c.execute('''INSERT INTO permissions (blob_id, user_id, readable_by, writable_by) VALUES (?, ?, ?, ?)''', (blob_id, user, 0, 1))
            conn.commit()
        else:
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
        '''Agregar permiso de lectura a un blob para un usuario y si no existe, crearlo'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT * FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user))
        permission = c.fetchone()
        if permission == None:
            c.execute('''INSERT INTO permissions (blob_id, user_id, readable_by, writable_by) VALUES (?, ?, ?, ?)''', (blob_id, user, 1, 0))
            conn.commit()
        else:
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
        if permission == None:
            return False
        else:
            return True
    
    def have_write_permission(self, blob_id, user):

        '''Verificar si un usuario tiene permiso de escritura'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT writable_by FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user))
        permission = c.fetchone()
        conn.close()
        if permission == None:
            return False
        else:
            return True
