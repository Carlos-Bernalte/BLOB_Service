#Scrip build
echo "*** Creando la imagen..."
docker build -f docker/restfs_auth/Dockerfile -t auth-service:latest docker/restfs_auth
docker build -f docker/restfs_blob/Dockerfile -t blob-service:latest docker/restfs_blob
docker build -f docker/restfs_dirs/Dockerfile -t dirs-service:latest docker/restfs_dirs
echo "\n*** Comprimiendo imagenes..."
docker save -o kubernetes/auth-service.tar auth-service:latest
docker save -o kubernetes/blob-service.tar blob-service:latest
docker save -o kubernetes/dirs-service.tar dirs-service:latest
echo "*** Imagen comprimida --> /kubernetes"