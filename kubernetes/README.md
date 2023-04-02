### Setting up MongoDB ReplicaSet on a Kubernetes StatefulSet

- Run mongo inside the first pod of the StatefulSet - `kubectl exec -it mongodb-rs-0 -- mongo`
- Create a config containing all the pods in the StatefulSet - `config = {_id:"rs0", version: 1, members: [{_id: 0, host: "mongodb-rs-0.mongodb-rs-service.default.svc.cluster.local:27017"}, {_id: 1, host: "mongodb-rs-1.mongodb-rs-service.default.svc.cluster.local:27017"}]}`
- Initate the ReplicaSet by running `rs.initiate(config)`
- Run mongo inside all the other pods one after another - `kubectl exec -it mongodb-rs-1 -- mongo` followed by `rs.slaveOk()` on each of them (sometimes it might take a while before the ReplicaSet is ready in the other pods, in which case, wait a little before running `rs.slaveOk()`)