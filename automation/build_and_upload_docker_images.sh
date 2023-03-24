# Login to docker using the service account key
cat $(git rev-parse --show-toplevel)/service_acc_keys/service-acc-key.json | docker login -u _json_key --password-stdin https://gcr.io

# Build and push the flask-server docker image onto GCR
docker build $(git rev-parse --show-toplevel)/flask-server -t gcr.io/eoscience/flask-server:latest
docker push gcr.io/eoscience/flask-server:latest
