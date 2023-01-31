'''Persistencia de datos en base de datos SQLite para manejar blobs'''
import sqlite3
import os
from werkzeug.datastructures import FileStorage
from common.constants import ADMIN, DB_NAME, STORAGE_DEFAULT, WRITABLE, READABLE
from common.errors import ObjectAlreadyExists, ObjectNotFound, Unauthorized, AlreadyDoneError


class BlobDB:
    '''Persistencia de datos en base de datos SQLite para manejar blobs'''

    def __init__(self, db_path=DB_NAME, storage_path=STORAGE_DEFAULT):
        '''Inicializar base de datos'''
        if not storage_path.endswith('/'):
            self.storage_path = storage_path+'/'
        else:
            self.storage_path = storage_path
        self.db_path = self.storage_path+db_path
        os.makedirs(self.storage_path, exist_ok=True)
        self._create_db()
        

    def _create_db(self):
        '''Crear base de datos'''
        print('SDASDASDASSDADdddd', self.db_path)
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS blobs (id STRING PRIMARY KEY, path TEXT)''')
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS permissions (id INTEGER PRIMARY KEY,blob_id STRING, user_id INTEGER, readable_by INTEGER, writable_by INTEGER)''')
        conn.close()

    def write_file(self, blob_id, blob_data):
        '''Escribir blob en disco'''
        blob_filename = os.path.join(self.storage_path, blob_id)
        if isinstance(blob_data, bytes):
            with open(blob_filename, 'wb') as contents:
                contents.write(blob_data)
        elif isinstance(blob_data, FileStorage): # pragma: no cover
            blob_data.save(blob_filename)
        return blob_filename

    def delete_file(self, path):
        '''Eliminar blob de disco'''
        if os.path.exists(path):
            os.remove(path)
        else:
            raise ObjectNotFound(path)

    def add_blob(self, blob_id, data, user):
        '''Agregar blob a la base de datos'''
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''SELECT path FROM blobs WHERE id=?''', (blob_id,))
        if cursor.fetchone() is not None:
            raise ObjectAlreadyExists(blob_id)
        local_filename = self.write_file(blob_id, data)
        conn.execute('''INSERT INTO blobs (id, path) VALUES (?,?)''',
                     (blob_id, local_filename,))
        if user is not ADMIN:
            conn.execute(
                '''INSERT INTO permissions (blob_id, user_id, readable_by, writable_by)
                 VALUES (?, ?, ?, ?)''', (blob_id, user, 1, 1))
        conn.commit()
        conn.close()
        return blob_id

    def exits_blob(self, blob_id):
        '''Obtener blob de la base de datos'''
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''SELECT path FROM blobs WHERE id=?''', (blob_id,))
        path = cursor.fetchone()
        conn.close()
        if path is None:
            raise ObjectNotFound(blob_id)
        return path[0]

    def remove_blob(self, blob_id, user):
        '''Eliminar blob de la base de datos'''
        path = self.exits_blob(blob_id)
        if not self.check_permissions(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has not permission')
        self.delete_file(path)
        conn = sqlite3.connect(self.db_path)
        conn.execute('''DELETE FROM blobs WHERE id=?''', (blob_id,))
        conn.execute(
            '''DELETE FROM permissions WHERE blob_id=? ''', (blob_id,))
        conn.commit()
        conn.close()

    def update_blob(self, blob_id, data, user):
        '''Actualizar blob'''
        path = self.exits_blob(blob_id)
        if not self.check_permissions(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has not permission')
        self.delete_file(path)
        local_filename = self.write_file(blob_id, data)
        conn = sqlite3.connect(self.db_path)
        conn.execute('''UPDATE blobs SET path=? WHERE id=?''',
                     (local_filename, blob_id))
        conn.commit()
        conn.close()

    def add_write_permission(self, blob_id, user, user_to_add):
        '''Agregar permiso de escritura a un blob para un usuario y si no existe, crearlo'''
        self.exits_blob(blob_id)
        if not self.check_permissions(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has not permission')
        if self.check_permissions(blob_id, user_to_add, WRITABLE):
            raise AlreadyDoneError('User already has permission', 204)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user_to_add))
        permission = cursor.fetchone()
        if permission is None:
            cursor.execute('''INSERT INTO permissions (blob_id, user_id, readable_by, writable_by)
                VALUES (?, ?, ?, ?)''', (blob_id, user_to_add, 0, 1))
            conn.commit()
        else:
            cursor.execute(
                '''UPDATE permissions SET writable_by=1 WHERE blob_id=? AND user_id=?''', (blob_id, user_to_add))
            conn.commit()
        conn.close()

    def revoke_write_permission(self, blob_id, user, user_to_revoke):
        '''Revocar permiso de escritura a un blob'''
        self.exits_blob(blob_id)
        if not self.check_permissions(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has not permission')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE permissions SET writable_by=0 WHERE blob_id=? AND user_id=?''', (blob_id, user_to_revoke))
        conn.commit()
        conn.close()

    def add_read_permission(self, blob_id, user, user_to_add):
        '''Agregar permiso de lectura a un blob para un usuario y si no existe, crearlo'''
        self.exits_blob(blob_id)
        if not self.check_permissions(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has not permission')
        if self.check_permissions(blob_id, user_to_add, READABLE):
            raise AlreadyDoneError('User already has permission', 204)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user_to_add))
        permission = cursor.fetchone()
        if permission is None:
            cursor.execute(
                '''INSERT INTO permissions (blob_id, user_id, readable_by, writable_by) VALUES (?, ?, ?, ?)''', (blob_id, user_to_add, 1, 0))
            conn.commit()
        else:
            cursor.execute(
                '''UPDATE permissions SET readable_by=1 WHERE blob_id=? AND user_id=?''', (blob_id, user_to_add))
            conn.commit()
        conn.close()

    def revoke_read_permission(self, blob_id, user, user_to_revoke):
        '''Revocar permiso de lectura a un blob'''
        self.exits_blob(blob_id)
        if not self.check_permissions(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has not permission')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''UPDATE permissions SET readable_by=0 WHERE blob_id=? AND user_id=?''', (blob_id, user_to_revoke))
        conn.commit()
        conn.close()

    def have_read_permission(self, blob_id, user):
        '''Verificar si un usuario tiene permiso de lectura'''
        self.exits_blob(blob_id)
        if user == ADMIN:
            return True
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''SELECT readable_by FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user))
        permission = cursor.fetchone()
        conn.close()
        if permission is None:
            return False
        if permission[0] == 0:
            return False
        return True

    def have_write_permission(self, blob_id, user):
        '''Verificar si un usuario tiene permiso de escritura'''
        self.exits_blob(blob_id)
        if user == ADMIN:
            return True
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''SELECT writable_by FROM permissions WHERE blob_id=? AND user_id=?''', (blob_id, user))
        permission = cursor.fetchone()
        conn.close()
        if permission is None:
            return False
        if permission[0] == 0:
            return False
        return True

    def check_permissions(self, blob_id, user, permission):
        ''' Chequea que el usuario tenga permiso de lectura o escritura sobre el blob'''
        if user == ADMIN:
            return True
        if permission == WRITABLE and self.have_write_permission(blob_id, user):
            return True
        if permission == READABLE and self.have_read_permission(blob_id, user):
            return True
        return False
