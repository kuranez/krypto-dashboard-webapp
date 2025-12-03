# Pushing Docker Image to GitHub Container Registry (GHCR)

## Quick Method (If You Have a Token)

```bash
# Set your GitHub token as an environment variable
export GITHUB_TOKEN="your_token_here"

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u kuranez --password-stdin

# Push the image
docker push ghcr.io/kuranez/krypto-dashboard-web:latest
```

## Using the Interactive Script

```bash
./push-to-ghcr.sh
```

The script will guide you through the process.

## Creating a GitHub Personal Access Token

1. **Go to:** https://github.com/settings/tokens/new

2. **Settings:**
   - **Note:** "Push Docker images to GHCR"
   - **Expiration:** Choose your preference (30 days, 90 days, or no expiration)

3. **Select scopes:**
   - ✅ `write:packages` (required)
   - ✅ `read:packages` (required)
   - ✅ `delete:packages` (optional)

4. **Click "Generate token"**

5. **Copy the token** (starts with `ghp_...`)
   - ⚠️ You won't be able to see it again!
   - Save it somewhere secure

## After Pushing

Once the image is pushed to GHCR:

### Option 1: Update Plesk to Pull Latest

In Plesk:
1. Docker → Stacks → krypto-dashboard-web
2. Click "Pull" or "Redeploy"
3. It will pull the latest image

### Option 2: Keep Using Build Config

If you prefer to keep building locally on the server:
- Continue using `docker-compose.build.yml`
- This avoids needing to push to GHCR

## Verify the Push

After pushing, verify at:
- https://github.com/kuranez/krypto-dashboard-web/pkgs/container/krypto-dashboard-web

You should see the latest version with today's date.

## Troubleshooting

### "denied: denied" Error
- Your token doesn't have the right permissions
- Create a new token with `write:packages` scope

### "unauthorized" Error
- Token is invalid or expired
- Create a new token

### DNS/Network Error
- Check your internet connection
- Try: `ping ghcr.io`

## Alternative: GitHub Actions

The repository already has a workflow at `.github/workflows/docker-publish.yml` that automatically builds and pushes when you push to `main`. However, it requires GitHub Actions to have network access to GHCR.

For manual control, use the methods above.
