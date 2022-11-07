'''
    Interfaces para el acceso a la API rest del servicio de blobs
'''

import requests
import json
import uuid


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

    def new_blob(self,local_filename, user):
        '''Crea un nuevo blob en formato json usando el usuario establecido'''
        blob_id = uuid.uuid4().hex
        with open(local_filename, 'rb') as f:
            req_body = {"file": {"filename": local_filename, "content": f.read().decode()}}
            response = requests.put(self.root+'v1/blob/'+blob_id,
                                    headers={'content-type': 'application/json','user-token': user},
                                    data=json.dumps(req_body)
                                    )
            if response.status_code == 201:
                return blob_id
            else:
                raise RestBlobError(response.text)
       
    def get_blob(self, blob_id, user):
        '''Descarga un blob usando el usuario dado'''
        response = requests.get( self.uri+'/v1/blob/'+blob_id ,  headers={'user-token': user})
        if response.status_code == 200:
            return response.json()

    def remove_blob(self, blob_id, user):
        '''Intenta eliminar un blob usando el usuario dado'''
        response = requests.delete(self.root+'/v1/blob/'+blob_id ,  headers={'user-token': user})
        
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')


class Blob:
    '''Cliente para controlar un blob'''
    def __init__(self, blob_id, blob_service, user):
        self.blob_id = blob_id
        self.blob_service = blob_service
        self.user = user
        
            
    @property
    def is_online(self):
        '''Comprueba si el blob existe'''
        response= requests.get(self.blob_service.root+'/v1/blob/'+self.blob_id, headers={'user-token': self.user})
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False

    def dump_to(self, local_filename):
        '''Vuelca los datos del blob en un archivo local'''
        response= requests.get(self.blob_service.root+'/v1/blob/'+self.blob_id, headers={'user-token': self.user})
        if response.status_code == 200:
            with open(local_filename, 'w') as f:
                f.write(response.text)
        else:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')

    def refresh_from(self, local_filename):
        '''Reemplaza el blob por el contenido del fichero local'''
        with open(local_filename, 'rb') as f:
            req_body = {"file": {"filename": local_filename, "content": f.read().decode()}}
            response = requests.post(self.blob_service.root+'v1/blob/'+self.blob_id,
                                    headers={'content-type': 'application/json','user-token': self.user},
                                    data=json.dumps(req_body)
                                    )
            if response.status_code == 200:
                return response.json()['blob_id']
            else:
                raise RestBlobError(response.text)
      

    def add_read_permission_to(self, user):
        '''Permite al usuario dado leer el blob'''
        response = response= requests.put(self.blob_service.root+'/v1/blob/'+self.blob_id+'/readable_by/'+user,  headers={'user-token': self.user})
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')

    def revoke_read_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de lectura'''
        response= requests.delete(self.blob_service.root+'/v1/blob/'+self.blob_id+'/readable_by/'+user,  headers={'user-token': self.user})
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')


    def add_write_permission_to(self, user):
        '''Permite al usuario dado escribir el blob'''
        response= requests.put(self.blob_service.root+'/v1/blob/'+self.blob_id+'/writable_by/'+user, headers={'user-token': self.user})
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')


    def revoke_write_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de escritura'''
        response= requests.delete(self.blob_service.root+'/v1/blob/'+self.blob_id+'/writable_by/'+user, headers={'user-token': self.user})
        if response.status_code != 200:
            raise RestBlobError(f'Unexpected status code: {response.status_code}')

