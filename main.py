from restfs import new_Blob, get_BlobService
import uuid
from time import sleep
def main():
    # 'http://0.0.0.0:3002'
    try:
        blob_service = get_BlobService('http://0.0.0.0:3002')
        blob=new_Blob(str(uuid.uuid4()), blob_service, '123')
        
        blob.refresh_from('requirements.txt')
        sleep(5)
        blob_service.remove_blob(blob.blob_id, '123')
        # blob.add_read_permission_to('nasty')
        # blob.add_write_permission_to('nasty')
        # blob2=new_Blob('f5f3fb04-c1ce-403f-bf5e-50548fb0e96d', blob_service, '123')
        # blob2.dump_to('descarga.txt')
        # blob_service.get_blob() 
    except Exception as e:
        print(e)
        print('Server not found')

if __name__ == '__main__':
    main()