# K8s

Authors
    :  [Carlos Bernalte García-Junco](https://github.com/Carlos-Bernalte)
    :  [Angel García Collado](https://github.com/theangelogarci)
# Contenido

- [Objetivo de la entrega](#objetivo-de-la-entrega)
- [Plataforma](#plataforma)
    - [Maquinas Virtuales](#maquinas-virtuales)
    - [Microk8s](#microk8s)
    - [Nodo director](#nodo-director)
    - [Nodo worker](#nodo-worker)
- [Despliegue](#despliegue)
    - [Requisitos](#requisitos)
    - [Script deplot.py](#script-deploy)


# Objetivo de la entrega
Una vez hemos implementado un servicio y lo hemos virtualizado, debemos trabajar en su despliegue y puesta en marcha.

El despliegue dependerá de la plataforma donde se va a ejecutar nuestro servicio, aunque el provisionamiento se puede realizar de manera independiente, usando shell scripts, por ejemplo.

Este ejercicio consta de dos partes: preparar la plataforma de despliegue y los propios scripts que la llevan a cabo.

No se va a pedir la automatización de la creación de la plataforma (aunque es un reto bastante interesante que el alumno puede llevar a cabo) siendo necesario únicamente los ficheros necesarios para crear la plataforma y una breve descripción de cómo montarla con dichos ficheros.

En cambio, el despliegue si se va a automatizar, para ello se escribirá un script llamado `deploy`. Para llevar a cabo el despliegue, deberá alimentarse el script con una serie de valores (IP’s, ficheros de entrada, etc.). El script deberá aceptar una opción “-h/--help” que mostrará toda la lista de variables y su significado. Dichas variables deberán poder establecerse en archivos de configuración o mediante opciones del script. El script puede estar implementado en cualquier lenguaje (shell, Python, etc.)
Repositorio:
```bash
git clone https://github.com/Carlos-Bernalte/BLOB_Service.git
```
# Plataforma
## Microk8s
La aplicación que utilizaremos para gestionar kubernetes es `microk8s v1.18.20` la cual incluye tanto un cliente para configurar los pods, nodos,... como tambien herramientas para añadir nodos al cluster de manera facil y sencilla.
## Maquinas Virtuales
Para la creación del cluster hemos optado por utilizar [Ubuntu Server 20.04 ](https://releases.ubuntu.com/20.04/) con los requisitos mencionados anteriormente. En el siguiente enlace adjuntamos ambas maquinas (la del `director` y el de `workers`) ya preconfiguradas con los paquetes y archivos necesarios (`setup.sh`) para su correcto funcionamiento:

- [enlace](https://github.com/)

A continución explicaremos como poner en funcionamiento el cluster ejecutando un par de comandos en los nodos `director` y el nodo `worker`. Se recomienda acceder a ellos vía `SSH` para copiar y pegar los comandos que se veran en la siguientes secciones.
- Nodo director-> login/password= director
- Nodo worker-> login/password= worker

## Nodo director
En la carpeta `$HOME` de `director` se encuentra el comando `setup.sh` el cual abrira los puertos necesarios para que podamos acceder a las herramientas del cluster. Tambien exportara la configuración del cluster en un archivo `config` al directorio creado `.kube`.
```bash
./setup.sh
```
## Nodo worker
Del script anterior dara como output un comando que nos facilitara conectarnos al cluester del nodo `director`. El formato del comando es parecido al siguiente:
```bash
microk8s join <ip-director>:25000/<token>
```

# Despliegue
## Requisitos
Necesitarmos `kubectl` para ello podemos intalarlo en nuestro ordandor con los siguientes comandos:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

Lo primordial sera poder ejecutar el script de despligue desde nuestro host, para ello tenemos de que traernos a nuestro host gracias a `SSH` el archivo `~/.kube/config` para luego exportarlo a la variable global y que nuestro `kubectl` tenga acceso a la `API`.
```bash
scp director@<ip-director>:/home/director/.kube/config .
export KUBECONFIG=$(echo config)
```
Luego ejecutaremos el siguiente comando esperando que la respuesta del `Server Version` no tenga fallos:
```bash
kubectl version
```

## Script deploy

```bash
python deploy.py
```
## Comandos chachis
```bash
sudo firewall-cmd --list-all
kubectl get all -A
```
```bash
kubectl apply -f ./deployment.yaml
kubectl expose deployment <> --type=NodePort
```