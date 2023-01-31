#Scrip build
echo "*** Creando la imagen..."
docker build -f docker/restfs_auth/Dockerfile -t auth-service:latest docker/restfs_auth
docker build -f docker/restfs_blob/Dockerfile -t blob-service:latest docker/restfs_blob
docker build -f docker/restfs_dirs/Dockerfile -t dirs-service:latest docker/restfs_dirs
echo "\n*** Comprimiendo imagenes..."
docker save auth-service:latest | gzip > kubernetes/auth-service.gz
docker save blob-service:latest | gzip > kubernetes/blob-service.gz
docker save dirs-service:latest | gzip > kubernetes/dirs-service.gz
echo "*** Imagen comprimida --> /kubernetes"