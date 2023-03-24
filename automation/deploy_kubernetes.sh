# Delete and recreate the key in case the service account has been updated.
kubectl delete secret gcr-key --ignore-not-found
kubectl create secret docker-registry gcr-key --docker-server=gcr.io --docker-username=_json_key --docker-password="$(cat ../service_acc_keys/eoscience-service-acc-key.json)"

kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "gcr-key"}]}'

# This deletes and recreates flask-server deployments/services.
if [ "$(kubectl get deployments | grep -c 'flask-server-deployment')" -ge 1 ]; then
    kubectl rollout restart deployment/flask-server-deployment
else
    kubectl create -f ../kubernetes/flask-server.yaml
fi

kubectl get pods
kubectl get services
kubectl describe service flask-server-service

# Run port forwarding to access the flask-server-service through a browser since our 
# service uses an internal only load balancer.
kubectl port-forward service/flask-server-service 8080:8080