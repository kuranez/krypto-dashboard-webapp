# Quick Commands Reference

## GitHub Setup

```bash
# Initialize and push to GitHub
git init
git add .
git commit -m "Initial commit: Cryptocurrency Dashboard Web"
git remote add origin https://github.com/kuranez/krypto-dashboard-web.git
git branch -M main
git push -u origin main
```

## Docker Commands

```bash
# Build locally
docker build -t krypto-dashboard-web .

# Run locally built image
docker run -p 5013:5013 krypto-dashboard-web

# Pull from GHCR
docker pull ghcr.io/kuranez/krypto-dashboard-web:latest

# Run from GHCR
docker run -p 5013:5013 ghcr.io/kuranez/krypto-dashboard-web:latest

# Run with API key
docker run -p 5013:5013 -e BINANCE_API_KEY=your_key ghcr.io/kuranez/krypto-dashboard-web:latest

# Use docker-compose
docker-compose up -d
docker-compose down
docker-compose logs -f
```

## Development

```bash
# Install dependencies
pip install -r web/app/requirements.txt

# Run locally for development
python launch.py

# Run with Panel serve
panel serve web/app/main.py --port 5013 --autoreload
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-dashboard

# Make changes, then commit
git add .
git commit -m "Add: new dashboard feature"

# Push to GitHub
git push origin feature/new-dashboard

# Create pull request on GitHub
```

## Release Tagging

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# This triggers multi-tagged Docker images:
# - ghcr.io/kuranez/krypto-dashboard-web:1.0.0
# - ghcr.io/kuranez/krypto-dashboard-web:1.0
# - ghcr.io/kuranez/krypto-dashboard-web:1
# - ghcr.io/kuranez/krypto-dashboard-web:latest
```

## Accessing the App

- **Local Development**: http://localhost:5007
- **Docker Container**: http://localhost:5013
- **With Prefix**: http://localhost:5013/krypto-dashboard

## Useful Links

- Repository: https://github.com/kuranez/krypto-dashboard-web
- Packages: https://github.com/kuranez?tab=packages
- Actions: https://github.com/kuranez/krypto-dashboard-web/actions
