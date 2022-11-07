
from restfs import new_Blob, get_BlobService

def main():
 
    try:
        blob_service = get_BlobService('http://127.0.0.1:3002')
        blob_id=blob_service.new_blob('requirements.txt', '123')
        print(blob_id)
        blob=new_Blob(blob_id, blob_service, '123')
        
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()