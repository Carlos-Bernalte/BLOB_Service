#Scrip build
echo "*** Creando la imagen..."
docker build -f docker/restfs_blob/Dockerfile -t blob-service:latest docker/restfs_blob
echo "\n*** Comprimiendo la imagen..."
docker save miapp | gzip > tar.gz
echo "*** Imagen comprimida --> tar.gz"