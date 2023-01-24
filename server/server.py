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
from common.errors import *
from common.constants import *

app = Flask('Blob Service')
AUTH = get_AuthService('0.0.0.0:3001')

def check_headers(headers):
    if headers.get(USER_TOKEN, None)!=None:
        token = headers.get(USER_TOKEN)
        return AUTH.user_of_token(token)
    elif headers.get(ADMIN_TOKEN, None)!=None:
        token = headers.get(ADMIN_TOKEN)
        if AUTH.is_admin(token):
            return ADMIN
        else:
            raise Unauthorized(token, 'Invalid admin token')
    else:
        raise MissingMandatoryArgument()


def check_permission(blob_id, user, permission):
    if user is ADMIN:
        return True
    if permission == WRITABLE and db.have_write_permission(blob_id, user):
        return True
    if permission == READABLE and db.have_read_permission(blob_id, user):
        return True
    return False


@app.route('/v1/blob/<blob_id>', methods=['GET'])
def get_blob(blob_id):
    try:
        user = check_headers(request.headers)

        blob_path = db.get_blob(blob_id)

        if not check_permission(blob_id, user, READABLE):
            raise Unauthorized(user, 'Has no permission')
        

        return send_from_directory(os.path.dirname(blob_path), os.path.basename(blob_path)), 200
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectNotFound as e:
        return make_response(str(e), 404)
    except Exception as e:
        print('[ERROR] ',e)
        return make_response(str(e), 500)
        

    
@app.route('/v1/blob/<blob_id>', methods=['PUT'])
def new_blob(blob_id):
    try:
        user = check_headers(request.headers)

        db.add_blob(blob_id, request.files[blob_id], user)
        return make_response('OK', 201)

    except MissingMandatoryArgument as e:
        return make_response(str(e), 400)
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectAlreadyExists as e:
        return make_response(str(e), 409)
    except Exception as e:
        print('[ERROR] ',e)
        return make_response(str(e), 500)


    
@app.route('/v1/blob/<blob_id>', methods=['POST'])
def update_blob(blob_id):
    try:
        user = check_headers(request.headers)
        
        blob_path=db.get_blob(blob_id)

        if not check_permission(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has no permission')

        db.update_blob(blob_id, request.files[blob_id])

    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectNotFound as e:
        return make_response(str(e), 404)
    except Exception as e:
        print('[ERROR] ',e)
        return make_response(str(e), 500)

@app.route('/v1/blob/<blob_id>', methods=['DELETE'])
def remove_blob(blob_id):

    try:
        user = check_headers(request.headers)
        db.get_blob(blob_id)
        if not check_permission(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has no permission')
        
        db.remove_blob(blob_id)


    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectNotFound as e:
        return make_response(str(e), 404)
    except Exception as e:
        print('[ERROR] ',e)
        return make_response(str(e), 500)


@app.route('/v1/blob/<blob_id>/writable_by/<user_priveleged>', methods=['PUT', 'DELETE'])
def write_permission(blob_id, user_priveleged):
    try:
        user = check_headers(request.headers)
        user_priveleged_id = AUTH.user_of_token(user_priveleged)
        db.get_blob(blob_id)
        if not check_permission(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has no permission')

        if request.method == 'PUT':
            if check_permission(blob_id, user_priveleged_id, WRITABLE):
                raise AlreadyDoneError(user_priveleged_id+ ' already has write permission.', 204)
            db.add_write_permission(blob_id, user_priveleged_id)
            return make_response('OK', 200)
        elif request.method == 'DELETE':
            if not check_permission(blob_id, user_priveleged_id, WRITABLE):
                raise AlreadyDoneError(user_priveleged_id+ ' already has no write permission.', 404)
            db.revoke_write_permission(blob_id, user_priveleged_id)
            return make_response('OK', 200)
        else:
            return make_response('Bad request', 300)
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectNotFound as e:
        return make_response(str(e), 404)
    except AlreadyDoneError as e:
        return make_response(str(e), e._status)
    except Exception as e:
        print('[ERROR] ',e)
        return make_response(str(e), 500)



@app.route('/v1/blob/<blob_id>/readable_by/<user_priveleged>', methods=['PUT', 'DELETE'])
def read_permission(blob_id, user_priveleged):

    try:
        user = check_headers(request.headers)
        user_priveleged_id = AUTH.user_of_token(user_priveleged)
        db.get_blob(blob_id)
        if not check_permission(blob_id, user, WRITABLE):
            raise Unauthorized(user, 'Has no permission')

        if request.method == 'PUT':
            if check_permission(blob_id, user_priveleged_id, READABLE):
                raise AlreadyDoneError(user_priveleged_id+ ' already has read permission.', 204)
            db.add_read_permission(blob_id, user_priveleged_id)
            return make_response('OK', 200)
        elif request.method == 'DELETE':
            if not check_permission(blob_id, user_priveleged_id, READABLE):
                raise AlreadyDoneError(user_priveleged_id+ ' already has no read permission.', 404)
            db.revoke_read_permission(blob_id, user_priveleged_id)
            return make_response('OK', 200)
        else:
            return make_response('Bad request', 300)
        
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectNotFound as e:
        return make_response(str(e), 404)
    except AlreadyDoneError as e:
        return make_response(str(e), e._status)
    except Exception as e:
        print('[ERROR] ',e)
        return make_response(str(e), 500)





def arg_parser():
    '''Parsea los argumentos de entrada'''
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--admin', type=str, default=secrets.token_hex(8),help='Token de administrador')
    parser.add_argument('-p', '--port', type=int, default=3002,help='Puerto para el servidor')
    parser.add_argument('-l', '--listening', type=str, default='0.0.0.0',help='Direccion de escucha')
    parser.add_argument('-d', '--db', type=str, default='./database.db',help='Base de datos')
    parser.add_argument('-s', '--storage', type=str, default='./storage/',help='Directorio de almacenamiento')

    return parser.parse_args()

def main():
    global app
    global db

    args = arg_parser()
    try:

        print('ADMIN TOKEN: {}'.format(args.admin))

        db = BlobDB(args.db, args.storage)

        app.run(host=args.listening, port=args.port, debug=True)
    except Exception as e:
        print('[ERROR] ',e.with_traceback())
        os.rmdir(args.storage)


if __name__ == '__main__':
    main()