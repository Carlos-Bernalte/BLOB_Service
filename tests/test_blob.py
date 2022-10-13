#!/usr/bin/env python3

import unittest

import blob.blob


class TestBlobImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        myblob = blob.blob.Blob()
        self.assertEqual(myblob.id, None)

    