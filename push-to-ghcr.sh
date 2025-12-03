#!/bin/bash
# Script to login to GitHub Container Registry and push the image

echo "=========================================="
echo "GitHub Container Registry Push Setup"
echo "=========================================="
echo ""
echo "You need a GitHub Personal Access Token (PAT) with 'write:packages' permission."
echo ""
echo "To create one:"
echo "1. Go to: https://github.com/settings/tokens/new"
echo "2. Note: 'Push Docker images to GHCR'"
echo "3. Select scopes:"
echo "   - ✓ write:packages"
echo "   - ✓ read:packages"
echo "   - ✓ delete:packages (optional)"
echo "4. Click 'Generate token'"
echo "5. Copy the token (it starts with 'ghp_...')"
echo ""
echo "=========================================="
echo ""

read -p "Do you have a GitHub token ready? (y/n): " has_token

if [ "$has_token" != "y" ]; then
    echo ""
    echo "Please create a token first, then run this script again."
    echo "Visit: https://github.com/settings/tokens/new"
    exit 0
fi

echo ""
read -sp "Enter your GitHub Personal Access Token: " GITHUB_TOKEN
echo ""
echo ""

echo "Logging in to ghcr.io..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u kuranez --password-stdin

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Login successful!"
    echo ""
    echo "Now pushing the image..."
    docker push ghcr.io/kuranez/krypto-dashboard-web:latest
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✅ SUCCESS! Image pushed to GHCR"
        echo "=========================================="
        echo ""
        echo "The image is now available at:"
        echo "ghcr.io/kuranez/krypto-dashboard-web:latest"
        echo ""
        echo "Next steps:"
        echo "1. In Plesk, pull the updated image"
        echo "2. Or set Plesk to use docker-compose.yml (it will auto-pull)"
        echo "3. Redeploy the stack"
        echo ""
    else
        echo ""
        echo "❌ Push failed. Check the error above."
    fi
else
    echo ""
    echo "❌ Login failed. Please check your token."
    exit 1
fi
