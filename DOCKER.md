# Docker and GitHub Container Registry Guide

## Quick Reference

### Build and Run Locally

```bash
# Build the image
docker build -t ghcr.io/kuranez/krypto-dashboard-app:latest .

# Run the container
docker run -p 5007:5007 ghcr.io/kuranez/krypto-dashboard-app:latest

# Run with API key
docker run -p 5007:5007 -e BINANCE_API_KEY=your_key ghcr.io/kuranez/krypto-dashboard-app:latest

# Run in detached mode
docker run -d -p 5007:5007 --name krypto-dashboard ghcr.io/kuranez/krypto-dashboard-app:latest
```

### Push to GitHub Container Registry (ghcr.io)

1. **Create a GitHub Personal Access Token (PAT)**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `write:packages`, `read:packages`, `delete:packages`
   - Copy the token

2. **Login to GitHub Container Registry**:
   ```bash
   echo YOUR_GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
   ```

3. **Build and tag the image**:
   ```bash
   docker build -t ghcr.io/kuranez/krypto-dashboard-app:latest .
   ```

4. **Push to registry**:
   ```bash
   docker push ghcr.io/kuranez/krypto-dashboard-app:latest
   ```

5. **Make the package public** (optional):
   - Go to https://github.com/users/kuranez/packages/container/krypto-dashboard-app
   - Click "Package settings"
   - Scroll to "Danger Zone"
   - Click "Change visibility" → "Public"

### Pull and Run from Registry

```bash
# Pull the latest image
docker pull ghcr.io/kuranez/krypto-dashboard-app:latest

# Run it
docker run -p 5007:5007 ghcr.io/kuranez/krypto-dashboard-app:latest
```

### Using Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Automated Publishing with GitHub Actions

The included `.github/workflows/docker-publish.yml` workflow automatically:
- Builds the Docker image on every push to main
- Tags it with multiple versions (latest, branch name, commit SHA)
- Publishes to ghcr.io automatically

To enable:
1. Push your code to GitHub
2. The workflow runs automatically - no additional setup needed!
3. Images will be available at: `ghcr.io/kuranez/krypto-dashboard-app`

### Tagging Strategy

The workflow automatically creates these tags:
- `latest` - most recent build from main branch
- `main` - latest from main branch
- `sha-abc123` - specific commit SHA
- `v1.0.0` - semantic version (if you push a git tag)

Example:
```bash
# Create a version tag
git tag v1.0.0
git push origin v1.0.0

# This will create image tags:
# - ghcr.io/kuranez/krypto-dashboard-app:latest
# - ghcr.io/kuranez/krypto-dashboard-app:v1.0.0
# - ghcr.io/kuranez/krypto-dashboard-app:1.0
# - ghcr.io/kuranez/krypto-dashboard-app:1
```

### Troubleshooting

**Permission denied when pushing:**
- Ensure your GitHub token has `write:packages` scope
- Check if you're logged in: `docker login ghcr.io`

**Image not found when pulling:**
- Package might be private - make it public in GitHub settings
- Or login first: `echo TOKEN | docker login ghcr.io -u USERNAME --password-stdin`

**Container exits immediately:**
- Check logs: `docker logs <container-id>`
- Run interactively: `docker run -it ghcr.io/kuranez/krypto-dashboard-app:latest /bin/bash`

**Port already in use:**
- Use a different host port: `docker run -p 8080:5007 ...`
- Or stop the conflicting container: `docker ps` then `docker stop <id>`
