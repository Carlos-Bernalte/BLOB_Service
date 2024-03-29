# Abrir puerto para añadir nodos al cluster
sudo firewall-cmd --zone=public --permanent --add-port 25000/tcp > /dev/null
sudo firewall-cmd --zone=public --permanent --add-port 16443/tcp > /dev/null
sudo systemctl restart firewalld.service > /dev/null
sudo docker load -i auth-service.tar
sudo docker load -i blob-service.tar
sudo docker load -i dirs-service.tar
sudo mkdir -p .kube
sudo microk8s config > .kube/config
sudo microk8s add-node
