#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST para el servicio de blobs
'''
import argparse
import os
import secrets

from flask import Flask, make_response, request, send_from_directory
from client import get_AuthService
from server.persistance import BlobDB
from common.errors import ObjectNotFound, ObjectAlreadyExists, Unauthorized, MissingMandatoryArgument, AlreadyDoneError
from common.constants import USER_TOKEN, ADMIN_TOKEN, ADMIN, WRITABLE, READABLE

APP = Flask('Blob Service')
AUTH = get_AuthService('0.0.0.0:3001')

def check_headers(headers):
    ''' Chequea que el header tenga un token de usuario o de admin'''
    if headers.get(USER_TOKEN, None) is not None:
        token = headers.get(USER_TOKEN)
        return AUTH.user_of_token(token)
    if headers.get(ADMIN_TOKEN, None) is not None:
        token = headers.get(ADMIN_TOKEN)
        if AUTH.is_admin(token):
            return ADMIN
        raise Unauthorized(token, 'Invalid admin token')
    raise MissingMandatoryArgument()

def check_permission(blob_id, user, permission):
    ''' Chequea que el usuario tenga permiso de lectura o escritura sobre el blob'''
    if user is ADMIN:
        return True
    if permission == WRITABLE and BLOB.have_write_permission(blob_id, user):
        return True
    if permission == READABLE and BLOB.have_read_permission(blob_id, user):
        return True
    return False

@APP.route('/v1/blob/<blob_id>', methods=['GET'])
def get_blob(blob_id):
    ''' Devuelve el blob con el id dado si el usuario tiene permiso de lectura o es admin'''
    try:
        user = check_headers(request.headers)
        blob_path = BLOB.get_blob(blob_id)
        if not check_permission(blob_id, user, READABLE):
            raise Unauthorized(user, 'Has no permission')
        return send_from_directory(os.path.dirname(blob_path), os.path.basename(blob_path)), 200
    except Unauthorized as error:
        return make_response(str(error), 401)
    except ObjectNotFound as error:
        return make_response(str(error), 404)
    except Exception as error: # pylint: disable=broad-except
        print('[ERROR] ', error)
        return make_response(str(error), 500)


@APP.route('/v1/blob/<blob_id>', methods=['PUT'])
def new_blob(blob_id):
    ''' Crea un nuevo blob con el id dado'''
    try:
        user = check_headers(request.headers)
        BLOB.add_blob(blob_id, request.files[blob_id], user)
        return make_response('OK', 201)
    except MissingMandatoryArgument as error:
        return make_response(str(error), 400)
    except Unauthorized as error:
        return make_response(str(error), 401)
    except ObjectAlreadyExists as error:
        return make_response(str(error), 409)
    except Exception as error: # pylint: disable=broad-except
        print('[ERROR] ', error)
        return make_response(str(error), 500)

@APP.route('/v1/blob/<blob_id>', methods=['POST'])
def update_blob(blob_id):
    ''' Actualiza el blob con el id dado'''
    try:
        user = check_headers(request.headers)
        BLOB.get_blob(blob_id)
        if not check_permission(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has no permission')
        BLOB.update_blob(blob_id, request.files[blob_id])
        return make_response('OK', 204)
    except Unauthorized as error:
        return make_response(str(error), 401)
    except ObjectNotFound as error:
        return make_response(str(error), 404)
    except Exception as error: # pylint: disable=broad-except
        print('[ERROR] ', error)
        return make_response(str(error), 500)

@APP.route('/v1/blob/<blob_id>', methods=['DELETE'])
def remove_blob(blob_id):
    ''' Elimina el blob con el id dado'''
    try:
        user = check_headers(request.headers)
        BLOB.get_blob(blob_id)
        if not check_permission(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has no permission')
        BLOB.remove_blob(blob_id)
        return make_response('OK', 200)
    except Unauthorized as error:
        return make_response(str(error), 401)
    except ObjectNotFound as error:
        return make_response(str(error), 404)
    except Exception as error: # pylint: disable=broad-except
        print('[ERROR] ', error)
        return make_response(str(error), 500)

@APP.route('/v1/blob/<blob_id>/writable_by/<user_priveleged>', methods=['PUT', 'DELETE'])
def write_permission(blob_id, user_priveleged): # pylint: disable=too-many-return-statements
    ''' Agrega o elimina permiso de escritura sobre el blob al usuario dado'''
    try:
        user = check_headers(request.headers)
        user_priveleged_id = AUTH.user_of_token(user_priveleged)
        BLOB.get_blob(blob_id)
        if not check_permission(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has no permission')
        if request.method == 'PUT':
            if check_permission(blob_id, user_priveleged_id, WRITABLE):
                raise AlreadyDoneError(
                    user_priveleged_id + ' already has write permission.', 204)
            BLOB.add_write_permission(blob_id, user_priveleged_id)
            return make_response('OK', 200)
        if request.method == 'DELETE':
            if not check_permission(blob_id, user_priveleged_id, WRITABLE):
                raise AlreadyDoneError(
                    user_priveleged_id + ' already has no write permission.', 404)
            BLOB.revoke_write_permission(blob_id, user_priveleged_id)
            return make_response('OK', 200)
        return make_response('Bad request', 300)
    except Unauthorized as error:
        return make_response(str(error), 401)
    except ObjectNotFound as error:
        return make_response(str(error), 404)
    except AlreadyDoneError as error:
        return make_response(str(error), error.status)
    except Exception as error: # pylint: disable=broad-except
        print('[ERROR] ', error)
        return make_response(str(error), 500)


@APP.route('/v1/blob/<blob_id>/readable_by/<user_priveleged>', methods=['PUT', 'DELETE'])
def read_permission(blob_id, user_priveleged): # pylint: disable=too-many-return-statements
    ''' Agrega o elimina permiso de lectura sobre el blob al usuario dado'''
    try:
        user = check_headers(request.headers)
        user_priveleged_id = AUTH.user_of_token(user_priveleged)
        BLOB.get_blob(blob_id)
        if not check_permission(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has no permission')
        if request.method == 'PUT':
            if check_permission(blob_id, user_priveleged_id, READABLE):
                raise AlreadyDoneError(
                    user_priveleged_id + ' already has read permission.', 204)
            BLOB.add_read_permission(blob_id, user_priveleged_id)
            return make_response('OK', 200)
        if request.method == 'DELETE':
            if not check_permission(blob_id, user_priveleged_id, READABLE):
                raise AlreadyDoneError(
                    user_priveleged_id + ' already has no read permission.', 404)
            BLOB.revoke_read_permission(blob_id, user_priveleged_id)
            return make_response('OK', 200)
        return make_response('Bad request', 300)
    except Unauthorized as error:
        return make_response(str(error), 401)
    except ObjectNotFound as error:
        return make_response(str(error), 404)
    except AlreadyDoneError as error:
        return make_response(str(error), error.status)
    except Exception as error: # pylint: disable=broad-except
        print('[ERROR] ', error)
        return make_response(str(error), 500)


def arg_parser():
    '''Parsea los argumentos de entrada'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--admin', type=str,
                        default=secrets.token_hex(8), help='Token de administrador')
    parser.add_argument('-p', '--port', type=int,
                        default=3002, help='Puerto para el servidor')
    parser.add_argument('-l', '--listening', type=str,
                        default='0.0.0.0', help='Direccion de escucha')
    parser.add_argument('-d', '--db', type=str,
                        default='./database.db', help='Base de datos')
    parser.add_argument('-s', '--storage', type=str,
                        default='./storage/', help='Directorio de almacenamiento')
    return parser.parse_args()


def main():
    '''Funcion principal'''
    global APP
    global BLOB
    args = arg_parser()
    try:
        print('ADMIN TOKEN: ',args.admin)
        BLOB = BlobDB(args.db, args.storage)
        APP.run(host=args.listening, port=args.port, debug=True)
    except Exception as error: # pylint: disable=broad-except
        print('[ERROR] ', error.with_traceback())
        os.rmdir(args.storage)

if __name__ == '__main__':
    main()
