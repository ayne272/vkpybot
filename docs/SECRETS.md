# Secret Management with SOPS

This project uses [SOPS](https://github.com/getsops/sops) with [age](https://github.com/FiloSottile/age) for encrypting Kubernetes secrets.

## Setup

Run the setup script:

```bash
./scripts/setup-sops.sh
```

This will:
- Install age and SOPS (macOS only, manual install needed for Linux)
- Generate an age encryption key
- Update `.sops.yaml` with your public key

## Usage

### Encrypt a secret file

```bash
sops -e -i k8s/secret.yaml
```

### Edit encrypted secret

```bash
sops k8s/secret.yaml
```

SOPS will decrypt it in your editor, then re-encrypt on save.

### Decrypt for viewing

```bash
sops -d k8s/secret.yaml
```

### Decrypt for kubectl apply

```bash
sops -d k8s/secret.yaml | kubectl apply -f -
```

## Pre-commit Hook

A git pre-commit hook automatically checks that all `k8s/secret*.yaml` files are encrypted before allowing commits. This prevents accidentally committing plaintext secrets.

## Key Management

- Private key location: `~/.config/sops/age/keys.txt`
- **IMPORTANT**: Backup this key securely! Without it, you cannot decrypt your secrets.
- Share the public key (in `.sops.yaml`) with team members who need to encrypt secrets.
- Never commit the private key to git.

## ArgoCD Integration

ArgoCD can decrypt SOPS-encrypted secrets automatically with KSOPS.

### Setup KSOPS in ArgoCD

1. Install KSOPS plugin in ArgoCD (see [../argocd/README.md](../argocd/README.md))

2. Add your age private key to ArgoCD:

```bash
kubectl create secret generic sops-age \
  --from-file=keys.txt=$HOME/.config/sops/age/keys.txt \
  -n argocd
```

3. Configure ArgoCD repo-server to use the key (see ArgoCD README)

### Manual Decryption for kubectl

If not using ArgoCD with KSOPS:
