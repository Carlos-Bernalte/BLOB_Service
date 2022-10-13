#!/usr/bin/env python3

'''
    Implementacion del servicio Blob
'''

class Blob:
    '''Implementa todas las operaciones sobre un objeto tipo Blob()'''

    def __init__(self):
        self.id = None
        self.ubi = None
        self.readable_by = []
        self.writable_by = []

    