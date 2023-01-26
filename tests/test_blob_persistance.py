import unittest
import tempfile
import uuid
import random
import os
from common.errors import *
from common.constants import DB_NAME

from server.persistance import BlobDB

USER1 = 'user1'
USER2 = 'user2'
ADMIN = 'admin'

BLOB_ID = str(uuid.uuid4())
WRONG_BLOB_ID = 'wrong_blob_id'

def _generate_random_bytes_(size=100):
    return random.randbytes(size)

class TestBlobImplementation(unittest.TestCase):
    
    def test_db_creation(self):
        '''Test initialization with folder'''
        with tempfile.TemporaryDirectory() as workspace:
            blobdb = BlobDB(storage_path=workspace)
            blobdb.initialize()
            self.assertTrue(os.path.exists(workspace+'/'+DB_NAME))

    def test_create_blob(self):
        '''Test creation of blob'''
        with tempfile.TemporaryDirectory() as workspace:
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobID=db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            self.assertEqual(blobID, BLOB_ID)

    def test_remove_blob(self):
        '''Test removing blob'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobID=db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            db.remove_blob(blobID, USER1)
            with self.assertRaises( ObjectNotFound):
                db.remove_blob(blobID, USER1)

                

    def test_remove_blob_wrong_id(self):    
        '''Test removing blob with wrong id'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobID=db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises( ObjectNotFound):
                db.remove_blob(WRONG_BLOB_ID, USER1)

    def test_remove_blob_wrong_user(self):    
        '''Test removing blob with wrong user'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobID=db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises( Unauthorized):
                db.remove_blob(blobID, USER2)

    def test_add_write_permission(self):
        '''Test adding write permission'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            self.assertFalse(db.have_write_permission(blobid, USER2))
            db.add_write_permission(blobid, USER1, USER2)
            self.assertTrue(db.have_write_permission(blobid, USER2))

    def test_add_read_permission(self):
        '''Test adding read permission'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            self.assertFalse(db.have_read_permission(blobid, USER2))
            db.add_read_permission(blobid, USER1, USER2)
            self.assertTrue(db.have_read_permission(blobid, USER2))

    def test_write_permission_wrong_blob(self):
        '''Test adding write permission with wrong blob id'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            bloblid=db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises(ObjectNotFound): 
                db.add_write_permission(WRONG_BLOB_ID, USER1, USER2)

    def test_read_permission_wrong_blob(self):
        '''Test adding read permission with wrong blob id'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid=db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises(ObjectNotFound):
                db.add_read_permission(WRONG_BLOB_ID, USER1, USER2)

    def test_write_permission_duplicated_user(self):    
        '''Test adding write permission with duplicated user'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            db.add_write_permission(blobid, USER1, USER2)
            self.assertTrue(db.have_write_permission(blobid, USER2))
            with self.assertRaises(AlreadyDoneError):
                db.add_write_permission(blobid, USER1, USER2)

    def test_read_permission_duplicated_user(self):    
        '''Test adding read permission with duplicated user'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            db.add_read_permission(blobid, USER1, USER2)
            self.assertTrue(db.have_read_permission(blobid, USER2))
            with self.assertRaises(AlreadyDoneError):
                db.add_read_permission(blobid, USER1, USER2)

    def test_write_permission_wrong_owner(self):    
        '''Test adding write permission with wrong owner'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises(Unauthorized):
                db.add_write_permission(blobid, USER2, USER1)

    def test_read_permission_wrong_owner(self):    
        '''Test adding read permission with wrong owner'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises(Unauthorized):
                db.add_read_permission(blobid, USER2, USER1)

    def test_remove_write_permission(self):
        '''Test removing write permission'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            db.add_write_permission(blobid, USER1, USER2)
            self.assertTrue(db.have_write_permission(blobid, USER2))
            db.revoke_write_permission(blobid, USER1, USER2)
            self.assertFalse(db.have_write_permission(blobid, USER2))
            
    def test_remove_read_permission(self):
        '''Test removing read permission'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            db.add_read_permission(blobid, USER1, USER2)
            self.assertTrue(db.have_read_permission(blobid, USER2))
            db.revoke_read_permission(blobid, USER1, USER2)
            self.assertFalse(db.have_read_permission(blobid, USER2))
            

    def test_remove_write_permission_admin(self):
        '''Test removing write permission as admin'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            self.assertTrue(db.have_write_permission(blobid, USER1))
            db.revoke_write_permission(blobid, ADMIN, USER1)
            self.assertFalse(db.have_write_permission(blobid, USER1))

    def test_remove_read_permission_admin(self):
        '''Test removing read permission as admin'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            self.assertTrue(db.have_read_permission(blobid, USER1))
            db.revoke_read_permission(blobid, ADMIN, USER1)
            self.assertFalse(db.have_read_permission(blobid, USER1))

    def test_remove_write_permission_wrong_blob(self):
        '''Test removing write permission with wrong blob id'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises(ObjectNotFound):
                db.revoke_write_permission(WRONG_BLOB_ID, USER1, USER2)
    
    def test_remove_read_permission_wrong_blob(self):
        '''Test removing read permission with wrong blob id'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises(ObjectNotFound):
                db.revoke_read_permission(WRONG_BLOB_ID, USER1, USER2)

    def test_remove_write_permission_unautorized(self):
        '''Test removing write permission to an user with already removed permission'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises(Unauthorized):
                db.revoke_write_permission(blobid, USER2, USER1)

    def test_remove_read_permission_unautorized(self):
        '''Test removing read permission to an user with already removed permission'''
        with tempfile.TemporaryDirectory() as workspace:    
            db = BlobDB(storage_path=workspace)
            db.initialize()
            blobid = db.add_blob(BLOB_ID,_generate_random_bytes_(), USER1)
            with self.assertRaises(Unauthorized):
                db.revoke_read_permission(blobid, USER2, USER1)

    

