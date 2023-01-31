#Script build
echo "*** Creando la imagen..."
docker build -f restfs_blob/Dockerfile -t blob-service:latest restfs_blob
echo "\n*** Comprimiendo la imagen..."
docker save blob-service:latest | gzip > tar.gz
echo "*** Imagen comprimida --> tar.gz"