
from client import get_BlobService, new_Blob
from random import randbytes
import requests
from requests.exceptions import HTTPError, ConnectionError
import tempfile
import os

URL = 'http://127.0.0.1:3002'
USER_TOKEN = 'u12345678'
ADMIN_TOKEN = 'a12345678'   
USER2_TOKEN = 'u2345678'
BLOBS=[]


def _generate_random_bytes_(size=100):
    return randbytes(size)


def create_blob_files(storage='/tmp'):
    files = []
    for test in range(3):
        data = _generate_random_bytes_()
        test_file = storage + f'/test{test}'
        with open(test_file, 'wb') as f:
            f.write(data)
        files.append(test_file)
    return files

def test_create_blobs(files, blob_service, user=USER_TOKEN):
    print('*** Test creating blobs')
    for file in files:
        blob_id = blob_service.new_blob(file, user)
        BLOBS.append(blob_id)
        print('[USER_TOKEN]:',user,' -- [BLOB]:',blob_id,' -- [FILE]: ', file)

def test_is_online(blob_service, user=USER_TOKEN):
    print('*** Test is_online')
    for blob in BLOBS:
        b=blob_service.get_blob(blob, user)
        if b.is_online:
            print('[BLOB]:',blob,' -- [ONLINE]')
        else:
            print('[BLOB]:',blob,' -- [OFFLINE]')

def test_dump_to(blob_service, path='./client/downloads',user=USER_TOKEN):
    print('*** Test dump_to')
    os.makedirs(path, exist_ok=True)
    for blob in BLOBS:
        b=blob_service.get_blob(blob, user)
        b.dump_to(path+'/'+b.blob_id)
        print('[BLOB]:',blob,' -- [DUMPED TO]: ', path)

def test_add_permission(blob_service, user_to_add, user=USER_TOKEN):
    print('*** Test add_permission')
    for blob in BLOBS:
        b=blob_service.get_blob(blob, user)
        b.add_read_permission_to(user_to_add)
        b.add_write_permission_to(user_to_add)

def test_revoke_permission(blob_service, user_to_revoke, user=USER_TOKEN):
    print('*** Test revoke_permission')

    b=blob_service.get_blob(BLOBS[0], user)
    b.revoke_read_permission_to(user_to_revoke)
    b.revoke_write_permission_to(user_to_revoke)

def test_refresh_blob(file,blob_service, user=USER_TOKEN):
    print('*** Test refresh_blob')
    for blob in BLOBS:
        b=blob_service.get_blob(blob, user)
        b.refresh_from(file)
        print('[BLOB]:',blob,' -- [REFRESHED]')

def test_remove_blob(blob_service,user=USER_TOKEN):
    print('*** Test remove_blob')
    for blob in BLOBS:
        blob_service.remove_blob(blob,user)
        print('[BLOB]:',blob,' -- [REMOVED]')

def test1():
    headers={'user-token':USER_TOKEN}
    # headers={'admin-token':ADMIN_TOKEN}
    response = requests.get(URL+'/v1/test', headers=headers)
    print(response.text)

def tests():
    
    files=create_blob_files(tempfile.mkdtemp())
    blob_service = get_BlobService(URL)

    test_create_blobs(files, blob_service)
    test_is_online(blob_service)
    test_dump_to(blob_service)
    test_add_permission(blob_service, USER2_TOKEN)
    test_revoke_permission(blob_service, USER2_TOKEN)
    test_refresh_blob('requirements.txt', blob_service)
    # test_remove_blob(blob_service)
    # test_is_online(blob_service)



if __name__ == '__main__':
    try:
        tests()
    except ConnectionError as e:
        print('[ERROR] No se puedo conectar al servidor: "',URL,'" Por favor compruebe que se esta ejecutando.')