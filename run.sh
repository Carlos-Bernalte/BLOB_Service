#Script run
echo "*** Ejecutando contenedor"
mkdir -p volume
docker run --privileged -ti -d --name blobs --hostname blobs_service -p 3002:3002 -v $(pwd)/volume:/storage miapp 