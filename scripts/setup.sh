# Abrir puerto para añadir nodos al cluster
sudo firewall-cmd --zone=public --permanent --add-port 25000/tcp > /dev/null
sudo firewall-cmd --zone=public --permanent --add-port 16443/tcp > /dev/null
sudo systemctl restart firewalld.service > /dev/null
mkdir -p .kube
microk8s config > .kube/config
export KUBECONFIG=$(echo .kube/config)
