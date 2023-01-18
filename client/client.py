
from client import get_BlobService, new_Blob
from random import randbytes
from requests.exceptions import HTTPError, ConnectionError
import tempfile
import os

URL = 'http://127.0.0.1:3002'
USER = '123'

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

def test_create_blobs(files, blob_service, user):
    print('*** Test creating blobs')
    for file in files:
        print('[FILE]',file)
        blob_id = blob_service.new_blob(file, user)
        print('[BLOB][',blob_id,'] created successfully')
        blob = new_Blob(blob_id, user, blob_service)
        blob
        # blob.refresh_from(file)
        # blob = blob_service.get_blob(blob_id, user)
        print(blob)


def tests():
    
    files=create_blob_files(tempfile.mkdtemp())
    blob_service = get_BlobService(URL)
    test_create_blobs(files, blob_service, USER)

    # blob_id=blob_service.new_blob('requirements.txt', USER)
    # print(blob_id)
    # blob1 = new_Blob(blob_id, USER, blob_service)

    # # blob1.add_write_permission_to('CARLOS')
    # blob1.revoke_write_permission_to('CARLOS')
    # blob = blob_service.get_blob(blob_id, USER)
    # print(blob)

    # # response = blob_service.remove_blob(blob_id, USER)
    # # print(response)



if __name__ == '__main__':
    try:
        tests()
    except ConnectionError as e:
        print('[ERROR] No se puedo conectar al servidor: "',URL,'" Por favor compruebe que se esta ejecutando.')