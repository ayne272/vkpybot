# Kubernetes manifests for vkpybot

## Deployment with ArgoCD (Recommended)

See [argocd/README.md](../argocd/README.md) for ArgoCD setup.

## Manual Deployment

**IMPORTANT**: Secrets must be encrypted with SOPS before committing. See [../docs/SECRETS.md](../docs/SECRETS.md).

Apply manifests in the following order:

```bash
kubectl apply -f namespace.yaml
kubectl apply -f secret.yaml
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f vkbot-deployment.yaml
```

Or apply all at once:

```bash
kubectl apply -f k8s/
```

## Files

- `namespace.yaml` - Namespace definition
- `secret.yaml` - Secrets for database and VK token
- `postgres-pvc.yaml` - Persistent volume claim for PostgreSQL
- `postgres-deployment.yaml` - PostgreSQL deployment
- `postgres-service.yaml` - PostgreSQL service
- `vkbot-deployment.yaml` - VK bot deployment

## Configuration

Before applying, update `secret.yaml` with your actual credentials.
