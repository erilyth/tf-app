# Delete and recreate the key in case the service account has been updated.
kubectl delete secret gcr-key --ignore-not-found
kubectl create secret docker-registry gcr-key --docker-server=gcr.io --docker-username=_json_key --docker-password="$(cat $(git rev-parse --show-toplevel)/service_acc_keys/service-acc-key.json)"

kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "gcr-key"}]}'

# This creates or restarts flask-server deployments/services.
if [ "$(kubectl get deployments | grep -c 'flask-server-deployment')" -ge 1 ]; then
    kubectl rollout restart deployment/flask-server-deployment
else
    kubectl create -f $(git rev-parse --show-toplevel)/kubernetes/flask-server.yaml
fi
if [ "$(kubectl get services | grep -c 'flask-server-service')" -lt 1 ]; then
    kubectl create -f $(git rev-parse --show-toplevel)/kubernetes/flask-server.yaml
fi

# This creates or restarts react-frontend deployments/services.
if [ "$(kubectl get deployments | grep -c 'react-frontend-deployment')" -ge 1 ]; then
    kubectl rollout restart deployment/react-frontend-deployment
else
    kubectl create -f $(git rev-parse --show-toplevel)/kubernetes/react-frontend.yaml
fi
if [ "$(kubectl get services | grep -c 'react-frontend-service')" -lt 1 ]; then
    kubectl create -f $(git rev-parse --show-toplevel)/kubernetes/react-frontend.yaml
fi

kubectl get pods
kubectl get services
kubectl describe service flask-server-service
kubectl describe service react-frontend-service

# Manually run port forwarding to access either of [flask-server-service, react-frontend-service]
# through a browser since our service uses an internal only load balancer. We use 8080 as the
# target port since all of our services are configured to run on 8080.
# kubectl port-forward service/<SERVICE_NAME> 8080:8080