#Script run
echo "*** Ejecutando contenedor"
mkdir -p volume
docker run -ti -d --name blob -p 3002:3002 -v $(pwd)/volume:/storage blob-service:latest