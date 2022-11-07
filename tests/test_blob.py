import unittest

from blob.blobDB import BlobDB


class TestBlobImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.id, None)

    def test_add_blob(self):
        '''Test adding blob'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.add_blob('1', 'testing', '1'), True)
    
    def test_remove_blob(self):
        '''Test removing blob'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.remove_blob('1'), True)

    def test_get_blob(self):
        '''Test getting blob'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.get_blob('1'), 'testing')
    
    def test_update_blob_path(self):
        '''Test updating blob'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.update_blob_path('1', 'testing2'), True)

    def test_add_write_permission(self):
        '''Test adding write permission'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.add_write_permission('1', '1'), True)

    def revoke_write_permission(self):
        '''Test revoking write permission'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.revoke_write_permission('1', '1'), True)

    def test_add_read_permission(self):
        '''Test adding read permission'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.add_read_permission('1', '1'), True)

    def test_revoke_read_permission(self):
        '''Test revoking read permission'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.revoke_read_permission('1', '1'), True)

    def test_have_read_permission(self):
        '''Test checking read permission'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.have_read_permission('1', '1'), True)

    def test_have_write_permission(self):
        '''Test checking write permission'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.have_write_permission('1', '1'), True)
    