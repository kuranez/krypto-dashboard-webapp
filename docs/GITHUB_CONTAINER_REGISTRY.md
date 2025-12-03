# GitHub Container Registry (GHCR) Guide

## Quick Commands

```bash
# Build image
docker-compose -f docker-compose.build.yml build

# Push to GHCR
docker push ghcr.io/kuranez/krypto-dashboard-web:latest

# Pull from GHCR
docker pull ghcr.io/kuranez/krypto-dashboard-web:latest
```

## Using the Push Script

```bash
./push-to-ghcr.sh
```

The script will guide you through the process.

## Creating a GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens/new

2. **Settings:**
   - **Note:** "Push Docker images to GHCR"
   - **Expiration:** Choose your preference

3. **Select scopes:**
   - ✅ `write:packages`
   - ✅ `read:packages`

4. **Generate and copy token** (starts with `ghp_...`)

## Manual Login

```bash
# Login to GHCR
echo YOUR_GITHUB_TOKEN | docker login ghcr.io -u kuranez --password-stdin

# Push image
docker push ghcr.io/kuranez/krypto-dashboard-web:latest
```

## Make Package Public

After first push:

1. Go to: https://github.com/kuranez?tab=packages
2. Click on `krypto-dashboard-web`
3. Click "Package settings"
4. Scroll to "Danger Zone"
5. Click "Change visibility" → "Public"

## GitHub Actions (Automatic)

The repository has a workflow at `.github/workflows/docker-publish.yml` that automatically builds and pushes when you push to `main`.

**To enable:**
- Just push to GitHub
- GitHub Actions builds and publishes automatically

## Verify Push

After pushing, check:
- https://github.com/kuranez/krypto-dashboard-web/pkgs/container/krypto-dashboard-web

You should see the latest version with today's date.

## Troubleshooting

**"denied" error:**
- Token lacks `write:packages` permission
- Create new token with correct scope

**"unauthorized" error:**
- Token is invalid or expired
- Create new token

**Cannot pull image:**
- Package might be private - make it public
- Or login first with your token
