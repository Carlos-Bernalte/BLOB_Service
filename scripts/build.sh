#Scrip build
echo "*** Creando la imagen..."
docker build --rm --tag miapp .
echo "\n*** Comprimiendo la imagen..."
docker save miapp | gzip > tar.gz
echo "*** Imagen comprimida --> tar.gz"