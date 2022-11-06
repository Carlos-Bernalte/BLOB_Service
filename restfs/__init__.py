#!/usr/bin/env python3

'''
    Factories for restfs client classes
'''

from typing import Union
from restfs.auth import AuthService, Administrator, User
from restfs.blob import BlobService, Blob
from restfs.directory import DirectoryService, Directory

def get_BlobService(uri:str) -> BlobService:
    return BlobService(uri)

## Blob service items ##

def new_Blob(blob_id:str, attached_service:BlobService, user:str) -> Blob:
    '''Given a blob identifier, a BlobService instance and the user, get intance of a Blob()'''
    return Blob(blob_id, attached_service, user)

