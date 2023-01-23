'''
    Interfaces para el acceso a la API rest del servicio de blobs
'''

import requests
import uuid
import os
from requests_toolbelt import MultipartEncoder



class RestBlobError(Exception): #Prgma: no cover
    '''Error caused by wrong responses from server'''
    def __init__(self, message='unknown'):
        self.msg = message

    def __str__(self):
        return f'RestBlobError: {self.msg}'
        
class BlobService:
    '''Cliente de acceso al servicio de blobbing'''
    def __init__(self,uri):
        self.root = uri
        if not self.root.endswith('/'):
            self.root = f'{self.root}/'
        self.root = self.root+'v1/blob/'

    def new_blob(self,local_filename, user):
        '''Crea un nuevo blob en formato json usando el usuario establecido'''
        blob_id = str(uuid.uuid4())
        headers={'user-token': user}

        mp = MultipartEncoder(
            fields={
                blob_id: (os.path.basename(local_filename), open(local_filename, 'rb'), 'application/octet-stream')
            }
        )
        headers['content-type'] = mp.content_type
        response = requests.put(self.root+blob_id, headers=headers, data=mp)

        if response.status_code == 201:
            return blob_id
        else:
            raise RestBlobError(response.text)
       
    def get_blob(self, blob_id, user):
        '''Descarga un blob usando el usuario dado'''
        return Blob(blob_id, self, user)

    def remove_blob(self, blob_id, user=None):
        '''Intenta eliminar un blob usando el usuario dado'''
        response = requests.delete(self.root+blob_id ,  headers={'user-token': user})
        
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')
        
        return response.text


class Blob:
    '''Cliente para controlar un blob'''
    def __init__(self, blob_id, blob_service=None, user=None):
        self.blob_id = blob_id
        self.blob_service = blob_service
        self.user = user
        self.blob_url = self.blob_service.root+self.blob_id
               
    @property
    def is_online(self):
        '''Comprueba si el blob existe'''
        if self.blob_service is None:
            return False
        response= requests.get(self.blob_url, headers={'user-token': self.user})
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        return False

    def dump_to(self, local_filename):
        '''Vuelca los datos del blob en un archivo local'''
        response= requests.get(self.blob_url, headers={'user-token': self.user})
        if response.status_code == 200:
            with open(local_filename, 'w') as f:
                f.write(response.text)
        else:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')

    def refresh_from(self, local_filename):
        '''Reemplaza el blob por el contenido del fichero local'''
        headers={'user-token': self.user}
        mp = MultipartEncoder(
            fields={
                self.blob_id: (os.path.basename(local_filename), open(local_filename, 'rb'), 'application/octet-stream')
            }
        )
        headers['content-type'] = mp.content_type
        response = requests.post(self.blob_url, headers=headers, data=mp)
        if response.ok:
            return response.text
        else:
            raise RestBlobError(response.text)
      
    def add_read_permission_to(self, user):
        '''Permite al usuario dado leer el blob'''
        response = response= requests.put(self.blob_url+'/readable_by/'+user,  headers={'user-token': self.user})
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')
        
    def revoke_read_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de lectura'''
        response= requests.delete(self.blob_url+'/readable_by/'+user,  headers={'user-token': self.user})
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')

    def add_write_permission_to(self, user):
        '''Permite al usuario dado escribir el blob'''
        response= requests.put(self.blob_url+'/writable_by/'+user, headers={'user-token': self.user})
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')

    def revoke_write_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de escritura'''
        response= requests.delete(self.blob_url+'/writable_by/'+user, headers={'user-token': self.user})
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')

    def __str__(self) -> str:
        return f'Blob #{self.blob_id}'

