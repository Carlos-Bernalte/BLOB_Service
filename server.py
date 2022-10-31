#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST para el servicio de blobs
'''
from flask import Flask, make_response, request
import os
import argparse
from blob.blob import BlobDB

app = Flask(__name__)


@app.route('/v1/blob/<int:blob_id>', methods=['GET'])
def get_blob(blob_id):
    raise NotImplementedError()

@app.route('/v1/blob', methods=['PUT'])
def new_blob():
    if not request.is_json:
        return make_response('Missing JSON', 400)
    if 'blob' not in request.get_json():
        return make_response('Missing "element" key', 400)
    blob = request.get_json()['blob']
    db.add_blob(blob['path'], 1)
    return make_response('OK', 200)


@app.route('/v1/blob/<int:blob_id>', methods=['DELETE'])
def remove_blob(blob_id):
    raise NotImplementedError()

@app.route('/v1/blob/<int:blob_id>', methods=['POST'])
def update_blob(blob_id):
    raise NotImplementedError()

@app.route('/v1/blob/<int:blob_id>/writable_by/<int:user>', methods=['PUT'])
def add_write_permission(blob_id, user):
    raise NotImplementedError()

@app.route('/v1/blob/<int:blob_id>/writable_by/<int:user>', methods=['DELETE'])
def remove_write_permission(blob_id, user):
    raise NotImplementedError()

@app.route('/v1/blob/<int:blob_id>/readable_by/<int:user>', methods=['PUT'])
def add_read_permission(blob_id, user):
    raise NotImplementedError()

@app.route('/v1/blob/<int:blob_id>/readable_by/<int:user>', methods=['DELETE'])
def remove_read_permission(blob_id, user):
    raise NotImplementedError()

def arg_parser():
    '''Parsea los argumentos de entrada'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--admin', type=int, default=1234,help='Token de administrador')
    parser.add_argument('-p', '--port', type=int, default=3002,help='Puerto para el servidor')
    parser.add_argument('-l', '--listening', type=str, default='0.0.0.0',help='Direccion de escucha')
    parser.add_argument('-d', '--db', type=str, default='./database.db',help='Base de datos')
    parser.add_argument('-s', '--storage', type=str, default='./storage',help='Directorio de almacenamiento')
    return parser.parse_args()

def main():
    global app
    global db

    args = arg_parser()
    if not os.path.exists(args.storage):
        os.makedirs(args.storage)

    db = BlobDB(args.db)

    app.run(host=args.listening, port=args.port, debug=True)

if __name__ == '__main__':
    main()