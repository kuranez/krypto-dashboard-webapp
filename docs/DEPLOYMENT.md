# Deployment Guide

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r web/requirements.txt

# Run locally
python web/app/launch.py
# Access at: http://localhost:5007
```

### Docker Deployment

#### Build and Push to GHCR
```bash
# Build image
docker-compose -f docker-compose.build.yml build

# Push to GitHub Container Registry
docker push ghcr.io/kuranez/krypto-dashboard-web:latest
```

#### Deploy on Server
```bash
# Pull latest image
docker-compose pull

# Start container
docker-compose up -d

# View logs
docker logs -f krypto-dashboard-web-krypto-dashboard-web-1
```

## Plesk Deployment

### 1. Configure Reverse Proxy

**Plesk → Domains → apps.kuracodez.space → Apache & Nginx Settings**

Add to **Additional nginx directives**:

```nginx
location /krypto-dashboard/ {
    proxy_pass http://127.0.0.1:5013/krypto-dashboard/;
    proxy_http_version 1.1;
    
    # WebSocket support
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    
    # Headers
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Timeouts
    proxy_connect_timeout 7d;
    proxy_send_timeout 7d;
    proxy_read_timeout 7d;
}
```

### 2. Deploy Container

```bash
# Navigate to repository
cd /var/www/vhosts/kuracodez.space/apps.kuracodez.space/repos/krypto-dashboard-web/

# Pull latest code
git pull origin main

# Pull latest image
docker-compose pull

# Restart container
docker-compose down && docker-compose up -d
```

### 3. Verify Deployment

**Access:** https://apps.kuracodez.space/krypto-dashboard

**Check logs:**
```bash
docker logs krypto-dashboard-web-krypto-dashboard-web-1
```

Expected output:
```
🚀 Starting Cryptocurrency Dashboard (Docker mode)...
📊 Server running on port 5013
🔗 Access at: http://0.0.0.0:5013/krypto-dashboard
```

## Environment Variables

Create `keys.env` file:
```bash
BINANCE_API_KEY=your_api_key_here
```

This file is automatically loaded by docker-compose.

## Troubleshooting

### Container Not Starting
```bash
# Check status
docker ps -a | grep krypto

# View logs
docker logs krypto-dashboard-web-krypto-dashboard-web-1

# Restart
docker-compose restart
```

### 404 Errors
- Verify nginx config is saved in Plesk
- Reload nginx: `service nginx reload`
- Check paths match: `/krypto-dashboard/` in both location and proxy_pass

### WebSocket Errors
- Ensure `Upgrade` and `Connection` headers are set in nginx
- Check browser console (F12) for connection errors

### Blank Page
- Check browser console for JavaScript errors
- Verify WebSocket connection established
- Test direct access: `curl http://127.0.0.1:5013/krypto-dashboard`

## Update Workflow

1. **Local changes:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```

2. **Build and push:**
   ```bash
   docker-compose -f docker-compose.build.yml build
   docker push ghcr.io/kuranez/krypto-dashboard-web:latest
   ```

3. **Deploy on server:**
   ```bash
   docker-compose pull
   docker-compose down && docker-compose up -d
   ```

## Access URLs

- **Local:** http://localhost:5007
- **Docker direct:** http://localhost:5013/krypto-dashboard
- **Production:** https://apps.kuracodez.space/krypto-dashboard
