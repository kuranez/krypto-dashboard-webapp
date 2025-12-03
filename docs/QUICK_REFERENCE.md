# Quick Reference

## Local Development

```bash
# Install dependencies
pip install -r web/requirements.txt

# Run locally
python web/app/launch.py
# Access at: http://localhost:5007
```

## Docker Commands

```bash
# Build
docker-compose -f docker-compose.build.yml build

# Run locally
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Push to GHCR
docker push ghcr.io/kuranez/krypto-dashboard-web:latest

# Pull from GHCR
docker pull ghcr.io/kuranez/krypto-dashboard-web:latest
```

## Git Workflow

```bash
# Make changes
git add .
git commit -m "Description of changes"
git push origin main

# Create release tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Server Deployment

```bash
# Pull latest code
git pull origin main

# Pull latest image
docker-compose pull

# Restart
docker-compose down && docker-compose up -d
```

## Access URLs

- **Local:** http://localhost:5007
- **Docker:** http://localhost:5013/krypto-dashboard
- **Production:** https://apps.kuracodez.space/krypto-dashboard

## Useful Links

- **Repository:** https://github.com/kuranez/krypto-dashboard-web
- **Packages:** https://github.com/kuranez?tab=packages
- **Actions:** https://github.com/kuranez/krypto-dashboard-web/actions
