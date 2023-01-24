'''
    Interfaces para el acceso a la API rest del servicio de autenticacion
'''
from common.errors import Unauthorized
from common.constants import USER_TOKEN, ADMIN_TOKEN

def header_name(user):
    '''Get proper header name or raise an error'''
    if user[0]=='u':
        return {USER_TOKEN: user}
    elif user[0]=='a':
        return {ADMIN_TOKEN: user}
    else:
        raise Unauthorized(user, 'No se ha identificado su header-token')


class Administrator:
    '''Cliente de autenticacion como administrador'''

    @property
    def token(self):
        '''Retorna el token del administrador'''
        raise NotImplementedError()

    def new_user(self, username, password):
        '''Crea un nuevo usuario'''
        raise NotImplementedError()

    def remove_user(self, username):
        '''Elimina un usuario'''
        raise NotImplementedError()


class User:
    '''Cliente de autenticacion como usuario'''

    def set_new_password(self, new_password):
        '''Cambia la contraseña del usuario'''
        raise NotImplementedError()

    @property
    def token(self):
        '''Retorna el token del usuario'''
        raise NotImplementedError()


class AuthService:
    '''Cliente de acceso al servicio de autenticacion'''
    def __init__(self, uri):
        self._uri_ = uri[:-1] if uri.endswith('/') else uri

    def user_of_token(self, token):
        if token == 'u12345678':
            return "usuario1"
        elif token == 'u2345678':
            return "usuario2"
        else:
            raise Unauthorized(token, 'User not found')

    def is_admin(self, token):
        if token == 'a12345678':
            return True
        else:
            False
            
    def exists_user(self, username):
        '''Return if given user exists or not'''
        raise NotImplementedError()

    def administrator_login(self, token):
        '''Return Adminitrator() object or error'''
        raise NotImplementedError()

    def user_login(self, username, password):
        '''Return User() object or error'''
        raise NotImplementedError()
