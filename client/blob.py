'''
    Interfaces para el acceso a la API rest del servicio de blobs
'''

import requests
import uuid
import os
from requests_toolbelt import MultipartEncoder
from common.constants import USER_TOKEN, ADMIN_TOKEN
from common.errors import Unauthorized, ObjectNotFound, UnexpectedError
from client.auth import header_name


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

        headers=header_name(user)

        mp = MultipartEncoder(
            fields={
                blob_id: (os.path.basename(local_filename), open(local_filename, 'rb'), 'application/octet-stream')
            }
        )
        headers['content-type'] = mp.content_type
        response = requests.put(self.root+blob_id, headers=headers, data=mp)

        if response.status_code not in [200, 201, 204]:
            raise Unauthorized(user.user, reason=response.content.decode('utf-8'))
        return Blob(blob_id, self, user)

       
    def get_blob(self, blob_id, user):
        '''Descarga un blob usando el usuario dado'''
        return Blob(blob_id, self, user)

    def remove_blob(self, blob_id, user=None):
        '''Intenta eliminar un blob usando el usuario dado'''
        headers=header_name(self.user)
        response = requests.delete(self.root+blob_id ,  headers=headers)
        
        if response.status_code == 404:
            raise Unauthorized(user.user, response.content.decode('utf-8'))
        if response.status_code not in [200, 204]:
            raise ObjectNotFound(f'Blob #{blob_id}')
        
def check_response(response, blob_id, user):
    if response.status_code == 404:
        raise ObjectNotFound(blob_id)
    if response.status_code == 401:
        raise Unauthorized(user, response.content.decode('utf-8'))
    if response.status_code not in [200, 201, 204]:
        raise UnexpectedError(response.content.decode('utf-8'))

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
        headers=header_name(self.user)
        if self.blob_service is None:
            return False
        response= requests.get(self.blob_url, headers=headers)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        return False

    def dump_to(self, local_filename):
        '''Vuelca los datos del blob en un archivo local'''
        headers=header_name(self.user)
        response= requests.get(self.blob_url, headers=headers)
        check_response(response, self.blob_id, self.user)
        with open(local_filename, 'w') as f:
            f.write(response.text)


    def refresh_from(self, local_filename):
        '''Reemplaza el blob por el contenido del fichero local'''
        headers=header_name(self.user)
        mp = MultipartEncoder(
            fields={
                self.blob_id: (os.path.basename(local_filename), open(local_filename, 'rb'), 'application/octet-stream')
            }
        )
        headers['content-type'] = mp.content_type
        response = requests.post(self.blob_url, headers=headers, data=mp)
        check_response(response, self.blob_id, self.user)

    def add_read_permission_to(self, user):
        '''Permite al usuario dado leer el blob'''
        headers=header_name(self.user)
        response = response= requests.put(self.blob_url+'/readable_by/'+user,  headers=headers)
        
        check_response(response, self.blob_id, self.user)
        
    def revoke_read_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de lectura'''
        headers=header_name(self.user)
        response= requests.delete(self.blob_url+'/readable_by/'+user,  headers=headers)
        check_response(response, self.blob_id, self.user)

    def add_write_permission_to(self, user):
        '''Permite al usuario dado escribir el blob'''
        headers=header_name(self.user)
        response= requests.put(self.blob_url+'/writable_by/'+user, headers=headers)
        
        check_response(response, self.blob_id, self.user)

    def revoke_write_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de escritura'''
        headers=header_name(self.user)
        response= requests.delete(self.blob_url+'/writable_by/'+user, headers=headers)
        
        check_response(response, self.blob_id, self.user)

    def __str__(self) -> str:
        return f'Blob #{self.blob_id}'

