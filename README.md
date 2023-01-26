# Blob Service

Authors
    :  [Carlos Bernalte García-Junco](https://github.com/Carlos-Bernalte)
    :  [Angel García Collado](https://github.com/theangelogarci)
## Contenido

- [Objetivo de la entrega](#objetivo-de-la-entrega)
- [Build](#build)
- [Run](#run)
- [Comprobar funcionamiento](#comprobar-funcionamiento)

## Objetivo de la entrega
En el ejercicio anterior creamos una serie de servicios accesibles mediante una API REST. Ahora se propone virtualizar el servicio de manera que pueda ser compilado y desplegado de manera automática.

Los servicios se podrán virtualizar mediante el uso de Docker o Vagrant. La generación de la imagen de docker o vagrant debe llevarse a cabo invocando a un script con nombre “build.sh” que no debe requerir ningún argumento. De permite que acepte opciones (muy recomendable documentarlas).

Además del script `build.sh` se incluirá otro script `run.sh` que ejecutará la virtualización (“docker run” o “vagrant up”) exponiendo el puerto del servicio. El puerto que se debe exponer será el puerto por defecto que debiera usar el servicio que se está virtualizando.

La imagen de docker debe tener un tamaño reducido, no siendo válidas imágenes de más de 1GB. El script `build.sh` deberá generar un archivo tar.gz con la imagen. Se puede usar cualquier imagen de origen teniendo en cuenta que la arquitectura de destino es x86_84.

Los datos persistentes del servicio se almacenarán en un volumen aparte, dicho volumen se podrá crear en el script `run.sh` si fuera necesario.

Repositorio:
```bash
git clone https://github.com/Carlos-Bernalte/BLOB_Service.git
```
## Build

Para la construcción de la imagen ejecutaremos el script `build.sh` que la cargara en función del Dockerfile.

```bash
./build.sh
```
Contenido del script:
```bash
#Script build
echo "*** Creando la imagen..."
docker build --rm --tag miapp .
echo "\n*** Comprimiendo la imagen..."
docker save miapp | gzip > tar.gz
echo "*** Imagen comprimida --> tar.gz"
```

## Run

Para lanzar el contenedor ejecutaremos el script `run.sh` el cual creara un directorio compartido entre el contenedor y nuestra maquina host.

```bash
./run.sh
```
Contenido del script:
```bash 
#Script run
echo "*** Ejecutando contenedor"
mkdir -p volume
docker run --privileged -ti -d --name blobs --hostname blobs_service -p 3002:3002 -v $(pwd)/volume:/storage miapp 
```

# Comprobar funcionamiento

Se puede comprobar el funcionamiento del contenedor corrriendo el cliente que lanzara unas pruebas al servidor que corre dentro y podremos ver que el volumen compartido (`volume`) se llena de archivos `blobs`.

**Recuerde tener el mismo los requisitos de la entrega anterior instalados ya sea en un entonto virtual o en tu maquina.*
```bash
python -m client.client
```
Un output como este se tiene que aparecer:
```bash
python -m client.client
*** Test creating blobs
[USER_TOKEN]: u12345678  -- [BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [FILE]:  /tmp/tmpztrh0ce0/test0
[USER_TOKEN]: u12345678  -- [BLOB]: 3606443d-d8cb-4492-ab14-01c67834bf47  -- [FILE]:  /tmp/tmpztrh0ce0/test1
[USER_TOKEN]: u12345678  -- [BLOB]: 65076540-bc64-46f5-a1ec-5efca81a12f9  -- [FILE]:  /tmp/tmpztrh0ce0/test2
*** Test is_online
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [ONLINE]
[BLOB]: 3606443d-d8cb-4492-ab14-01c67834bf47  -- [ONLINE]
[BLOB]: 65076540-bc64-46f5-a1ec-5efca81a12f9  -- [ONLINE]
*** Test dump_to
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [DUMPED TO]:  ./client/downloads
[BLOB]: 3606443d-d8cb-4492-ab14-01c67834bf47  -- [DUMPED TO]:  ./client/downloads
[BLOB]: 65076540-bc64-46f5-a1ec-5efca81a12f9  -- [DUMPED TO]:  ./client/downloads
*** Test add_permission
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [ADDED READ PERMISION TO]  u2345678
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [ADDED READ PERMISION TO]  u2345678
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [ADDED READ PERMISION TO]  u2345678
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [ADDED READ PERMISION TO]  u2345678
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [ADDED READ PERMISION TO]  u2345678
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [ADDED READ PERMISION TO]  u2345678
*** Test revoke_permission
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [REVOKED READ PERMISION TO]  u2345678
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [REVOKED WRITE PERMISION TO]  u2345678
*** Test refresh_blob
[BLOB]: 3606443d-d8cb-4492-ab14-01c67834bf47  -- [REFRESHED]
*** Test remove_blob
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [REMOVED]
*** Test is_online
[BLOB]: e4f4bfa1-e275-4750-b3bd-82380785205b  -- [OFFLINE]
[BLOB]: 3606443d-d8cb-4492-ab14-01c67834bf47  -- [ONLINE]
[BLOB]: 65076540-bc64-46f5-a1ec-5efca81a12f9  -- [ONLINE]
```



