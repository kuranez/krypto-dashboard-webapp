# Docker Compose Deployment Guide for Plesk

## Prerequisites

### 1. Make GitHub Package Public

The Docker image at `ghcr.io/kuranez/krypto-dashboard-web:latest` must be public to pull without authentication.

**Steps:**
1. Go to https://github.com/kuranez?tab=packages
2. Click on `krypto-dashboard-web`
3. Click "Package settings" (right sidebar)
4. Scroll to "Danger Zone"
5. Click "Change visibility" → Select "Public"
6. Confirm the change

### 2. Alternative: Authenticate Docker in Plesk

If you want to keep the package private:

1. Create a GitHub Personal Access Token with `read:packages` permission
2. In Plesk server, run:
   ```bash
   echo YOUR_GITHUB_TOKEN | docker login ghcr.io -u kuranez --password-stdin
   ```

## Deployment Options

### Option 1: Use Pre-built Image (Recommended for Production)

Use the simplified `docker-compose.yml` that only pulls the pre-built image:

```yaml
services:
  krypto-dashboard-web:
    image: ghcr.io/kuranez/krypto-dashboard-web:latest
    user: "10000:1003"
    ports:
      - "5013:5013"
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
      - BINANCE_API_KEY=${BINANCE_API_KEY:-}
    restart: unless-stopped
```

**This is the current `docker-compose.yml` in the repository.**

### Option 2: Build from Source in Plesk

If you want Plesk to build the image, ensure the repository is properly cloned with the `web/` directory structure.

Use `docker-compose.build.yml`:

```yaml
services:
  krypto-dashboard-web:
    build:
      context: .
      dockerfile: Dockerfile
    image: ghcr.io/kuranez/krypto-dashboard-web:latest
    user: "10000:1003"
    ports:
      - "5013:5013"
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
      - BINANCE_API_KEY=${BINANCE_API_KEY:-}
    restart: unless-stopped
```

## Plesk Deployment Steps

### Using Plesk Docker Extension

1. **Install Docker Extension** (if not already installed)
   - Extensions → Docker → Install

2. **Add Stack**
   - Docker → Stacks → Add Stack
   - **Name**: krypto-dashboard-web
   - **Repository**: https://github.com/kuranez/krypto-dashboard-web.git
   - **Branch**: main
   - **Compose file**: docker-compose.yml

3. **Set Environment Variables** (optional)
   - Add `BINANCE_API_KEY` if needed

4. **Deploy**
   - Click "Deploy"
   - Wait for the image to pull and container to start

### Using Plesk Git/Repository

If Plesk clones the repository to `/var/www/vhosts/kuracodez.space/apps.kuracodez.space/repos/krypto-dashboard-web/`:

```bash
cd /var/www/vhosts/kuracodez.space/apps.kuracodez.space/repos/krypto-dashboard-web/
docker compose up -d
```

## Troubleshooting

### Error: "unauthorized" when pulling

**Solution**: Make the GitHub package public (see Prerequisites above)

### Error: "web/requirements.txt not found" when building

**Cause**: Repository not fully cloned or using build mode when it should use pre-built image

**Solution**: 
- Use the simplified `docker-compose.yml` (without `build:`)
- OR ensure the repository is properly cloned with all directories

### Error: "version is obsolete"

**Solution**: Remove `version: '3.8'` from docker-compose.yml (already done)

### Container doesn't start

Check logs:
```bash
docker compose logs krypto-dashboard-web
```

## Access the Application

Once deployed:
- **Direct access**: http://apps.kuracodez.space:5013
- **With prefix**: http://apps.kuracodez.space:5013/krypto-dashboard

Configure your reverse proxy/web server to forward requests to port 5013.

## Update Deployment

When you push updates to GitHub:

1. GitHub Actions automatically builds and pushes new image
2. In Plesk, pull the latest image:
   ```bash
   docker compose pull
   docker compose up -d
   ```

Or in Plesk Docker Extension:
- Stacks → krypto-dashboard-web → Redeploy
