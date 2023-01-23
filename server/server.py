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

    if headers.get('user-token', None)!=None:
        token = headers.get('user-token')
        return AUTH.user_of_token(token)
    elif headers.get('admin-token', None)!=None:
        token = headers.get('admin-token')
        if AUTH.is_admin(token):
            return ADMIN
    else:
        raise Unauthorized()
    return None

def check_permission(blob_id, user, permission):
    if permission == WRITABLE and db.have_write_permission(blob_id, user):
        return True
    if permission == READABLE and db.have_read_permission(blob_id, user):
        return True
    return False


@app.route('/v1/blob/<blob_id>', methods=['GET'])
def get_blob(blob_id):
    try:
        user = check_headers(request.headers)
        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

        return send_from_directory(os.path.dirname(blob), os.path.basename(blob)), 200
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectAlreadyExists as e:
        return make_response(str(e), 409)

    
@app.route('/v1/blob/<blob_id>', methods=['PUT'])
def new_blob(blob_id):
    try:
        user = check_headers(request.headers)

        db.add_blob(blob_id, request.files[blob_id], user)
        return make_response('OK', 201)

    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectAlreadyExists as e:
        return make_response(str(e), 409)


    
@app.route('/v1/blob/<blob_id>', methods=['POST'])
def update_blob(blob_id):
    try:
        user = check_headers(request.headers)
        
        if db.update_blob(blob_id, request.files[blob_id]):
            return make_response('OK', 201)
        else:
            return make_response('Error', 500)
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectAlreadyExists as e:
        return make_response(str(e), 409)


@app.route('/v1/blob/<blob_id>', methods=['DELETE'])
def remove_blob(blob_id):

    try:
        user = check_headers(request.headers)
    
        blob=db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

        if db.remove_blob(blob_id):
            return make_response('OK', 200)
        else:
            return make_response('Error', 500)
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectAlreadyExists as e:
        return make_response(str(e), 409)


@app.route('/v1/blob/<blob_id>/writable_by/<user_priveleged>', methods=['PUT', 'DELETE'])
def add_write_permission(blob_id, user_priveleged):
    try:
        user = check_headers(request.headers)
    
        if request.method == 'PUT':
            db.add_write_permission(blob_id, user_priveleged)
            return make_response('OK', 200)
        elif request.method == 'DELETE':
            db.revoke_write_permission(blob_id, user_priveleged)
            return make_response('OK', 200)
        else:
            return make_response('Bad request', 300)
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectAlreadyExists as e:
        return make_response(str(e), 409)



@app.route('/v1/blob/<blob_id>/readable_by/<user_priveleged>', methods=['PUT', 'DELETE'])
def add_read_permission(blob_id, user_priveleged):

    try:
        user = check_headers(request.headers)

        if request.method == 'PUT':
            db.add_read_permission(blob_id, user_priveleged)
            return make_response('OK', 200)
        elif request.method == 'DELETE':
            db.revoke_read_permission(blob_id, user_priveleged)
            return make_response('OK', 200)
        else:
            return make_response('Bad request', 300)
        
    except Unauthorized as e:
        return make_response(str(e), 401)
    except ObjectAlreadyExists as e:
        return make_response(str(e), 409)





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