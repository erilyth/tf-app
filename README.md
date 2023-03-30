### Setup

- Run the following steps to setup the project initially.
- Update the git config to point git hooks to ./git_hooks by running `git config core.hooksPath git_hooks`. This allows us to automatically run Docker and Kubernetes deployment hooks upon a git push.
- Create a service account for the GCP project you are currently using and ensure it has access to read/write from all cloud buckets since this is required when the initial GCR bucket is created upon the first Docker image push to GCR.
- Download the service account key and place it under `service_acc_keys/service-acc-key.json`
- Authenticate gcloud using the service account key `gcloud auth activate-service-account [ACCOUNT] --key-file=service_acc_keys/service-acc-key.json`
- Install npm on your machine
- Install Docker on your machine
- Install Kubernetes (kubectl) on your machine
- Connect Kubernetes to a GCP Kubernetes cluster by running `gcloud container clusters get-credentials CLUSTER_NAME --region=COMPUTE_REGION`

### Usage

- You can run automation scripts present in `automation/` (which are also automatically run upon a `git push origin main`) to deploy changes onto the Kubernetes cluster
- If you make any changes to the MongoDB StatefulSet, then you will have to follow the additional instructions present in `kubernetes/README.md` to setup the MongoDB ReplicaSet.
- Currently react-frontend is unable to access the flask-server-service directly from the cluster when you test it on a local browser with port forwarding. Hence, for development, port-forward both the react-frontend-service as well as the flask-server-service and make API calls to `localhost:<PORT_OF_FLASK_SERVER_SERVICE>` from within the react app. Command for doing this is - `kubectl port-forward service/flask-server-service 5000:5000, service/react-frontend-service 3000:3000`

### TODOs

- Add some colored text to make it easier to know whats going on when the automation scripts are run
- Support authentication/authorization
- Add in a cache to the system