# Push commands to the background, when the script exits, the commands will exit too
kubectl port-forward service/flask-server-service 5000:5000 & \
kubectl port-forward service/react-frontend-service 3000:3000 & \

echo "Press CTRL-C to stop port forwarding and exit the script"
wait