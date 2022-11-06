#!/usr/bin/env python3

import unittest

import blob.blobDB


class TestBlobImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        myblob = blobDB.blobDB.Blob()
        self.assertEqual(myblob.id, None)

    