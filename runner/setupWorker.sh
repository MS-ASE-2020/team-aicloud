kubectl delete replicaset worker
docker build -t kalineid/worker -f Dockerfile_worker .
docker push kalineid/worker
kubectl apply -f worker.yaml
