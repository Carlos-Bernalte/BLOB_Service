#!/usr/bin/env python3

import unittest

from blob.blobDB import BlobDB


class TestBlobImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        db = BlobDB('testing.db', 'testing_storage')
        self.assertEqual(db.id, None)

    