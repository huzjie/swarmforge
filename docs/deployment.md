# Deployment

## Docker
```bash
docker-compose up -d
```

## Kubernetes
```bash
kubectl apply -f deploy/k8s/
```

## Helm
```bash
helm install swarmforge ./deploy/helm/swarmforge
```