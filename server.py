#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST para el servicio de blobs
'''
from flask import Flask, make_response, request, send_from_directory
import os
import argparse
from blob.blobDB import BlobDB
import secrets

app = Flask('Blob Service')

def user_of_token(token):
    if token == '123':
        # print(token)
        return "usuario_test"
    else:
        return None

def write_file(blob, storage_path):
    new_path = storage_path
    paths = blob['filename'].split('/')

    for path in paths:
        if path == paths[-1]:
            open(new_path + '/' + path, 'wb').write(blob['content'].encode())
        else:
            new_path = os.path.join(new_path, path)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                
    return os.path.join(storage_path, blob['filename'])

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print('No existe el archivo')    

def check_header_tokens(request, blob_id):
    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
   
    user = user_of_token(request.headers['user-token'])
    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        pass
    else:
        
        if user is None:
            return make_response('Invalid user-token', 401)
        elif not db.have_write_permission(blob_id, request.headers['user-token']):
            return make_response('No write permission', 401)

        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

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

        if db.have_read_permission(blob_id, request.headers['user-token']):
            path = db.get_blob(blob_id)
            return send_from_directory(os.path.dirname(path), os.path.basename(path))
        else:
            return make_response('No read permission', 401)      
    
    
@app.route('/v1/blob/<blob_id>', methods=['PUT', 'POST'])
def new_blob(blob_id):
    if not request.is_json:
        return make_response('No JSON provided', 400)

    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
    user = user_of_token(request.headers['user-token'])

    if user is None:
        return make_response('Invalid user-token', 401)

    blob = write_file(request.get_json()['file'], args.storage)

    if db.add_blob(blob_id, blob, user):
        
        return make_response('OK', 200)
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

    blob_updated=write_file(request.get_json()['file'], args.storage)
    delete_file(blob)

    if db.update_blob_path(int(blob_id), blob_updated):
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
    delete_file(blob)
    if db.remove_blob(blob_id):
        return make_response('OK', 200)
    else:
        return make_response('Error', 500)


@app.route('/v1/blob/<blob_id>/writable_by/<user_priveleged>', methods=['PUT'])
def add_write_permission(blob_id, user_priveleged):
    
    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
   
    user = user_of_token(request.headers['user-token'])
    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        pass
    else:
        
        if user is None:
            return make_response('Invalid user-token', 401)
        elif not db.have_write_permission(blob_id, request.headers['user-token']):
            return make_response('No write permission', 401)
            
        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

    db.add_write_permission(blob_id, user_priveleged)
    return make_response('OK', 200)

@app.route('/v1/blob/<blob_id>/writable_by/<user_priveleged>', methods=['DELETE'])
def remove_write_permission(blob_id, user_priveleged):
    
    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
   
    user = user_of_token(request.headers['user-token'])
    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        pass
    else:
        
        if user is None:
            return make_response('Invalid user-token', 401)
        elif not db.have_write_permission(blob_id, request.headers['user-token']):
            return make_response('No write permission', 401)
            
        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

    db.revoke_write_permission(blob_id, user_priveleged)
    return make_response('OK', 200)

@app.route('/v1/blob/<blob_id>/readable_by/<user_priveleged>', methods=['PUT'])
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
        elif not db.have_write_permission(blob_id, request.headers['user-token']):
            return make_response('No write permission', 401)
            
        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

    db.add_read_permission(blob_id, user_priveleged)
    return make_response('OK', 200)

@app.route('/v1/blob/<blob_id>/readable_by/<user_priveleged>', methods=['DELETE'])
def remove_read_permission(blob_id, user_priveleged):

    if 'user-token' not in request.headers:
        return make_response('No user-token provided', 401)
   
    user = user_of_token(request.headers['user-token'])
    if 'admin-token' in request.headers:
        # Check admin token Todo: implementar request.headers['user-token'] == args.admin
        pass
    else:
        
        if user is None:
            return make_response('Invalid user-token', 401)
        elif not db.have_write_permission(blob_id, request.headers['user-token']):
            return make_response('No write permission', 401)
            
        blob = db.get_blob(blob_id)
        if blob is None:
            return make_response('Blob not found', 404)

    db.revoke_read_permission(blob_id, user_priveleged)
    return make_response('OK', 200)


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
    except Exception:
        print('Bye')
        os.rmdir(args.storage)


if __name__ == '__main__':
    main()