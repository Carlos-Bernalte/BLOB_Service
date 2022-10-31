'''
    Interfaces para el acceso a la API rest del servicio de blobs
'''
from urllib import request
import requests
import json
import server



class BlobService:
    '''Cliente de acceso al servicio de blobbing'''
    def __init__(self,uri,timeout=120):
        self.uri=uri
        self.timeout=timeout

    def new_blob(self, local_filename, user):
        '''Crea un nuevo blob usando el usuario establecido'''
        resp= requests.put(self.uri+'/v1/blob', data={'user':user})

    def get_blob(self, blob_id, user):
        '''Obtiene un blob usando el usuario indicado'''
        resp= requests.get(self.uri+'/v1/blob/<int:blob_id>'+str(blob_id), data={'user':user})

    def remove_blob(self, blob_id, user):
        '''Intenta eliminar un blob usando el usuario dado'''
        resp= requests.delete(self.uri+'/v1/blob/<int:blob_id>'+str(blob_id), data={'user':user})


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
        raise NotImplementedError()

    def dump_to(self, local_filename):
        '''Vuelca los datos del blob en un archivo local'''
        raise NotImplementedError()

    def refresh_from(self, local_filename):
        '''Reemplaza el blob por el contenido del fichero local'''
        raise NotImplementedError()

    def add_read_permission_to(self, user):
        '''Permite al usuario dado leer el blob'''
        resp= request.put(self.uri+'/v1/blob/<int:blob_id>/readable_by/', data={'user':user})

    def revoke_read_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de lectura'''
        resp= requests.delete(self.uri+'/v1/blob/<int:blob_id>/readable_by/', data={'user':user})

    def add_write_permission_to(self, user):
        '''Permite al usuario dado escribir el blob'''
        resp= request.put(self.uri+'/v1/blob/<int:blob_id>/writable_by/', data={'user':user})

    def revoke_write_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de escritura'''
        resp= requests.delete(self.uri+'/v1/blob/<int:blob_id>/writable_by/', data={'user':user})



def main():
    '''Funcion principal'''
    # Creamos un cliente para el servicio de blobbing
    client = BlobService('http://0.0.0.0:3002')
    client.new_blob('test.txt', 'user1')
    cabeceras={'user-token': 'admin' , 'user-token': 'user' } 
    pass

if __name__ == '__main__':
    main()