#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST para el servicio de blobs
'''
import argparse
import os
import secrets

from flask import Flask, make_response, request, send_from_directory, jsonify

from server.service import BlobDB
# from common.errors import BlobError

app = Flask('Blob Service')


def check_headers(headers):
    if 'user-token' not in headers:
        return make_response('No user-token provided', 401)
    user = user_of_token(headers['user-token'])
    if user is None:
        return make_response('Invalid user-token', 401)
    return user

@app.route('/v1/blob/<blob_id>', methods=['GET'])
def get_blob(blob_id):
    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
    user = user_of_token(request.headers['user-token'])

    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        path= db.get_blob(blob_id)
        return send_from_directory(os.path.dirname(path), os.path.basename(path))
    else:
        if user is None:
            return make_response('Invalid user-token', 401)
        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

        if db.have_read_permission(blob_id, user):
            return send_from_directory(os.path.dirname(blob), os.path.basename(blob)), 200
        else:
            return make_response('No read permission', 401)       
    
@app.route('/v1/blob/<blob_id>', methods=['PUT'])
def new_blob(blob_id):

    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
    user = user_of_token(request.headers['user-token'])

    if user is None:
        return make_response('Invalid user-token', 401)
    
    if db.add_blob(blob_id, request.files[blob_id], user):
        return make_response('OK', 201)
    else:
        return make_response('Error', 500)
    
@app.route('/v1/blob/<blob_id>', methods=['POST'])
def update_blob(blob_id):

    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
    user = user_of_token(request.headers['user-token'])

    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        pass
    else:
        if user is None:
            return make_response('Invalid user-token', 401)

        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

    blob=db.get_blob(blob_id)
    if blob is None:
        return make_response('Blob not found', 404)

    if 'file' not in request.get_json():
        return make_response('No file provided', 400)
    if 'filename' not in request.get_json()['file'] or 'content' not in request.get_json()['file']:
        return make_response('No file provided', 400)

    if db.update_blob_path(blob_id, request.get_json()['file']):
        return make_response('OK', 200)
    else:
        return make_response('Error', 500)

@app.route('/v1/blob/<blob_id>', methods=['DELETE'])
def remove_blob(blob_id):

    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
    user = user_of_token(request.headers['user-token'])

    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        pass
    else:
        if user is None:
            return make_response('Invalid user-token', 401)
        elif not db.have_write_permission(blob_id, user):
            return make_response('No write permission', 401)

        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)
    
    blob=db.get_blob(blob_id)
    if blob is None:
        return make_response('Blob not found', 404)
    if db.remove_blob(blob_id):
        return make_response('OK', 200)
    else:
        return make_response('Error', 500)

@app.route('/v1/blob/<blob_id>/writable_by/<user_priveleged>', methods=['PUT', 'DELETE'])
def add_write_permission(blob_id, user_priveleged):
    
    print('METODO: ',request.method)
    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
   
    user = user_of_token(request.headers['user-token'])
    print(user)
    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        pass
    else:
        
        if user is None:
            return make_response('Invalid user-token', 401)
        elif not db.have_write_permission(blob_id, user):
            return make_response('No write permission', 402)
            
        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)
    
    if request.method == 'PUT':
        db.add_write_permission(blob_id, user_priveleged)
        return make_response('OK', 200)
    elif request.method == 'DELETE':
        db.revoke_write_permission(blob_id, user_priveleged)
        return make_response('OK', 200)
    else:
        return make_response('Bad request', 300)


@app.route('/v1/blob/<blob_id>/readable_by/<user_priveleged>', methods=['PUT', 'DELETE'])
def add_read_permission(blob_id, user_priveleged):

    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
    user = user_of_token(request.headers['user-token'])
    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        pass
    else:
        if user is None:
            return make_response('Invalid user-token', 401)
        elif not db.have_write_permission(blob_id, user):
            return make_response('No write permission', 401)
            
        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)
    if request.method == 'PUT':
        db.add_read_permission(blob_id, user_priveleged)
        return make_response('OK', 200)
    elif request.method == 'DELETE':
        db.revoke_read_permission(blob_id, user_priveleged)
        return make_response('OK', 200)
    else:
        return make_response('Bad request', 300)


def user_of_token(token):
    if token == '123':
        # print(token)
        return "usuario_test"
    else:
        return None



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
    global args
    args = arg_parser()
    try:

        print('ADMIN TOKEN: {}'.format(args.admin))
        if not os.path.exists(args.storage):
            os.makedirs(args.storage)

        db = BlobDB(args.db, args.storage)

        app.run(host=args.listening, port=args.port, debug=True)
    except Exception as e:
        print('Error: {}'.format(e.traceback.format_exc()))
        os.rmdir(args.storage)


if __name__ == '__main__':
    main()