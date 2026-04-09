# ArgoCD Application

This directory contains ArgoCD application manifest for automated deployment with SOPS-encrypted secrets.

## Prerequisites

1. ArgoCD installed in your cluster
2. KSOPS plugin installed in ArgoCD (see below)
3. Age private key configured in ArgoCD
4. Repository access configured in ArgoCD
5. Docker image published to container registry

## Install KSOPS in ArgoCD

KSOPS allows ArgoCD to decrypt SOPS-encrypted secrets automatically.

### Option 1: Using argocd-vault-plugin (Recommended)

```bash
# Install argocd-vault-plugin with SOPS support
kubectl apply -f https://raw.githubusercontent.com/argoproj-labs/argocd-vault-plugin/main/manifests/cmp-sidecar/kustomize/cmp-plugin.yaml
```

### Option 2: Custom ArgoCD image with KSOPS

Create a custom ArgoCD repo-server image:

```dockerfile
FROM argoproj/argocd:latest

USER root
RUN apt-get update && apt-get install -y curl && \
    curl -Lo /usr/local/bin/ksops https://github.com/viaduct-ai/kustomize-sops/releases/latest/download/ksops_latest_Linux_x86_64 && \
    chmod +x /usr/local/bin/ksops && \
    curl -Lo /usr/local/bin/sops https://github.com/getsops/sops/releases/latest/download/sops-latest.linux.amd64 && \
    chmod +x /usr/local/bin/sops

USER argocd
```

## Configure Age Key in ArgoCD

Create a secret with your age private key:

```bash
# Get your age private key
cat ~/.config/sops/age/keys.txt

# Create secret in ArgoCD namespace
kubectl create secret generic sops-age \
  --from-file=keys.txt=$HOME/.config/sops/age/keys.txt \
  -n argocd

# Patch argocd-repo-server to mount the key
kubectl patch deployment argocd-repo-server -n argocd --type='json' \
  -p='[
    {
      "op": "add",
      "path": "/spec/template/spec/volumes/-",
      "value": {
        "name": "sops-age",
        "secret": {"secretName": "sops-age"}
      }
    },
    {
      "op": "add",
      "path": "/spec/template/spec/containers/0/volumeMounts/-",
      "value": {
        "name": "sops-age",
        "mountPath": "/home/argocd/.config/sops/age",
        "readOnly": true
      }
    },
    {
      "op": "add",
      "path": "/spec/template/spec/containers/0/env/-",
      "value": {
        "name": "SOPS_AGE_KEY_FILE",
        "value": "/home/argocd/.config/sops/age/keys.txt"
      }
    }
  ]'
```

## Setup

1. Update `application.yaml` if needed:
   - Repository: `https://github.com/ayne272/vkpybot.git`
   - Adjust `targetRevision` if needed (branch/tag)

2. Docker image will be published to: `ghcr.io/ayne272/vkpybot`

3. Apply ArgoCD application:
```bash
kubectl apply -f argocd/application.yaml
```

## Features

- **Automated sync**: Changes in git automatically deployed
- **Self-healing**: Automatically reverts manual changes
- **Pruning**: Removes resources deleted from git
- **Retry logic**: Automatic retry on sync failures
- **Namespace creation**: Creates namespace if not exists

## Access ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Then open: https://localhost:8080

## Manual Sync

```bash
argocd app sync vkbot
```

## Check Status

```bash
argocd app get vkbot
```
