kubectl delete services auth-service
kubectl delete services blob-service
kubectl delete services dirs-service

kubectl delete deployments.apps auth
kubectl delete deployments.apps blob
kubectl delete deployments.apps dirs