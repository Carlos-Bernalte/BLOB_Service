'''
    Interfaces para el acceso a la API rest del servicio de blobs
'''
from email import header
from urllib import request
import requests
import json
import server

headersList1 = {
 "user-token": "123"
}
headersList2 = {
 "admin token": "1234"
}

class BlobService:
    '''Cliente de acceso al servicio de blobbing'''
    def __init__(self,uri,timeout=120):
        self.uri=uri
        self.timeout=timeout

    def new_blob(self, local_filename, user):
        '''Crea un nuevo blob usando el usuario establecido'''
        payload = json.dumps({"path": "nombre.txt"})
        response = requests.request("PUT", self.uri+'/v1/blob', data=payload,  headers=headersList1)
        print (response.text)

    def get_blob(self, blob_id, user):
        '''Obtiene un blob usando el usuario indicado'''
        response = requests.request("GET", self.uri+'/v1/blob' ,  headers=headersList1)
        print (response.text)

    def remove_blob(self, blob_id, user):
        '''Intenta eliminar un blob usando el usuario dado'''
        response = requests.request("DELETE", self.uri+'/v1/blob' ,  headers=headersList1)
        print (response.text)


class Blob:
    '''Cliente para controlar un blob'''
    def __init__(self, blob_id, path, read_users, write_users):
        '''Crea una instancia de Blob'''
        self.id = blob_id
        self.path = path
        self.readers = read_users
        self.writers = write_users

    @property
    def is_online(self):
        '''Comprueba si el blob existe'''
        if self==None:
            return False
        else:
            if (response = requests.request("GET", self.uri+'/v1/blob' ,  headers=headersList1)==200):
                return True

    def dump_to(self, local_filename):
        '''Vuelca los datos del blob en un archivo local'''
        response = requests.request("GET", self.uri+'/v1/blob' ,  headers=headersList1)
        getBlob = requests.get(self.uri+'/v1/blob/<int:blob_id>')
        open("/dumps/<int:blob_id>", "wb").write(getBlob.content)

    def refresh_from(self, local_filename):
        '''Reemplaza el blob por el contenido del fichero local'''
        response = requests.request("PUT", self.uri+'/v1/blob/<int:blob_id>',  headers=headersList1)
        refreshFrom= requests.put(self.uri+'/v1/blob/<int:blob_id>', data=open("/dumps/<int:blob_id>", "rb"))

    def add_read_permission_to(self, user):
        '''Permite al usuario dado leer el blob'''
        response = requests.request("PUT", self.uri+'/v1/blob/<int:blob_id>/readable_by/',  headers=headersList1)
        print (response.text)

    def revoke_read_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de lectura'''
        response= requests.delete(self.uri+'/v1/blob/<int:blob_id>/readable_by/',  headers=headersList1)
        print (response.text)

    def add_write_permission_to(self, user):
        '''Permite al usuario dado escribir el blob'''
        response= requests.put(self.uri+'/v1/blob/<int:blob_id>/writable_by/', headers=headersList1)
        print (response.text)


    def revoke_write_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de escritura'''
        response= requests.delete(self.uri+'/v1/blob/<int:blob_id>/writable_by/', headers=headersList1)
        print (response.text)



def main():
    '''Funcion principal'''
    # Creamos un cliente para el servicio de blobbing
    client = BlobService('http://0.0.0.0:3002')
    client.new_blob('test.txt', 'user1')
    pass

if __name__ == '__main__':
    main()