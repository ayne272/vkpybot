#!/bin/bash
# Install KSOPS in ArgoCD

echo "Installing KSOPS in ArgoCD..."

# Create custom argocd-repo-server with KSOPS
kubectl patch deployment argocd-repo-server -n argocd --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/initContainers/-",
    "value": {
      "name": "install-ksops",
      "image": "viaductoss/ksops:v4.3.1",
      "command": ["/bin/sh", "-c"],
      "args": ["cp /usr/local/bin/ksops /custom-tools/"],
      "volumeMounts": [{
        "mountPath": "/custom-tools",
        "name": "custom-tools"
      }]
    }
  },
  {
    "op": "add",
    "path": "/spec/template/spec/volumes/-",
    "value": {
      "name": "custom-tools",
      "emptyDir": {}
    }
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/volumeMounts/-",
    "value": {
      "mountPath": "/usr/local/bin/ksops",
      "name": "custom-tools",
      "subPath": "ksops"
    }
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/env/-",
    "value": {
      "name": "XDG_CONFIG_HOME",
      "value": "/home/argocd/.config"
    }
  }
]'

echo "KSOPS installed! Restart repo-server to apply changes."
