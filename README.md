# Blob Service
Authors
    :  [Carlos Bernalte García-Junco](https://github.com/Carlos-Bernalte)
    :  [Angel García Collado](https://github.com/theangelogarci)

## Contenido
- [Objetivo de la entrega](#objetivo-de-la-entrega-1)
- [Preparación entorno virtual](#preparación-entorno-virtual)
- [Requisitos](#instalación-de-requisitos)
- [Ejecutar servidor y cliente](#ejecutar-servidor-y-cliente)
- [Pylint, Pysec y cobertura del servicio]()
## Objetivo de la entrega 1
Se deberá implementar una API REST que permita la gestión básica de blobs o paquetes de bytes. El lenguaje de implementación es libre, aunque se recomienda utilizar Python 3. Además, deberá crearse una librería y un cliente en Python 3 para poder utilizar el servicio sin necesidad de conocer la propia API REST.

Repositorio:
```bash
git clone https://github.com/Carlos-Bernalte/BLOB_Service.git
```
## Preparación entorno virtual
Si el usuario lo desea, puede preparar un entorno virtual para instalar todos los requisitos que necesita el servicio de `Blobs` sin necesidad de alterar los paquetes ya instalados en un maquina:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalación de requisitos
Los paquetes necesarios para el funcionamiento del servicio pueden ser instalados con el siguiente:
```bash
pip install -r requirements.txt
```

## Ejecutar servidor y cliente
Puedes ejecutar el servidor con el siquiente comando, aun asi el script del servidor (con la opción -h) acepta argumentos para configurar de manera mas específica (si no incluyes ninguno tomara valores por defecto)


```bash
python3 -m server.server -h 
usage: server.py [-h] [-a ADMIN] [-p PORT] [-l LISTENING] [-d DB] [-s STORAGE]

options:
  -h, --help            show this help message and exit
  -a ADMIN, --admin ADMIN
                        Token de administrador
  -p PORT, --port PORT  Puerto para el servidor
  -l LISTENING, --listening LISTENING
                        Direccion de escucha
  -d DB, --db DB        Base de datos
  -s STORAGE, --storage STORAGE
                        Directorio de almacenamiento
```
```bash
python3 -m server.server
```

El cliente ejecutara una serie de llamadas secuenciales al servidor para comprobar que todo funciona:
```bash
python3 -m client.client
```
## Pylint, Pysec y cobertura del servicio
Todas las pruebas referentes al servicio se puedes ejecutar de manera automática con el comando `tox`. Esto tambien tendra como resultado una serie de reportes que se podran ver en la carpeta `/tests`.
```bash
tox
```
