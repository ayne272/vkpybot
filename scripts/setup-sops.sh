#!/bin/bash
# Setup script for SOPS encryption

set -e

echo "Setting up SOPS for secret encryption..."

# Check if age is installed
if ! command -v age &> /dev/null; then
    echo "Installing age..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install age
    else
        echo "Please install age manually: https://github.com/FiloSottile/age"
        exit 1
    fi
fi

# Check if sops is installed
if ! command -v sops &> /dev/null; then
    echo "Installing SOPS..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install sops
    else
        echo "Please install SOPS manually: https://github.com/getsops/sops/releases"
        exit 1
    fi
fi

# Generate age key if not exists
AGE_KEY_FILE="$HOME/.config/sops/age/keys.txt"
if [ ! -f "$AGE_KEY_FILE" ]; then
    echo "Generating age key..."
    mkdir -p "$(dirname "$AGE_KEY_FILE")"
    age-keygen -o "$AGE_KEY_FILE"
    echo "Age key generated at: $AGE_KEY_FILE"
fi

# Get public key
PUBLIC_KEY=$(grep "# public key:" "$AGE_KEY_FILE" | awk '{print $4}')
echo "Your public key: $PUBLIC_KEY"

# Update .sops.yaml with the public key
sed -i.bak "s/age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/$PUBLIC_KEY/g" .sops.yaml
rm .sops.yaml.bak

echo ""
echo "✓ SOPS setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit k8s/secret.yaml with your actual secrets"
echo "2. Encrypt it: sops -e -i k8s/secret.yaml"
echo "3. Commit the encrypted file"
echo ""
echo "To edit encrypted file: sops k8s/secret.yaml"
echo "To decrypt for viewing: sops -d k8s/secret.yaml"
