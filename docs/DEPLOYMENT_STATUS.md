# Deployment Status

## ✅ Current Configuration

### Container Details
- **Image**: `ghcr.io/kuranez/krypto-dashboard-web:latest`
- **Port**: 5013
- **URL Path**: `/krypto-dashboard/app`
- **Status**: Running and responding with HTTP 200

### Serving Configuration
```
App serves at: http://0.0.0.0:5013/krypto-dashboard/app
```

This matches the pattern of your other Panel apps:
- `/qr-code-generator/` on port 5010
- `/eu-energy-map/app` on port 5011 ✅ (same pattern)
- `/krypto-dashboard/app` on port 5013 ✅ (new)

### Nginx Configuration (Already Set in Plesk)
```nginx
location /krypto-dashboard/ {
    proxy_pass http://localhost:5013/krypto-dashboard/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # WebSocket support
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Access URLs
- **Public**: `https://apps.kuracodez.space/krypto-dashboard/app`
- **Direct (server)**: `http://127.0.0.1:5013/krypto-dashboard/app`

## Environment Variables

Loaded from `keys.env` file:
```yaml
env_file:
  - keys.env
```

The `keys.env` file should contain:
```bash
BINANCE_API_KEY=your_actual_key_here
```

## Logging Differences

### Your EU Energy Map (Bokeh server):
```
2025-11-23 16:22:13,981 Starting Bokeh server version 3.7.3 (running on Tornado 6.5.1)
2025-11-23 16:22:13,985 Bokeh app running at: http://0.0.0.0:5011/eu-energy-map/app
```

### Krypto Dashboard (Panel serve):
```
🚀 Starting Cryptocurrency Dashboard (Docker mode)...
📊 Server running on port 5013
🔗 Access at: http://0.0.0.0:5013/krypto-dashboard/app
Launching server at http://0.0.0.0:5013
```

**Note:** Panel's `pn.serve()` has different logging than standalone Bokeh server. Both work correctly - it's just a display difference.

## Testing Commands

From the server (SSH):
```bash
# Check container status
docker ps | grep krypto

# Test endpoint
curl -I http://127.0.0.1:5013/krypto-dashboard/app

# View logs
docker logs krypto-dashboard-web_krypto-dashboard-web_1

# Restart
docker-compose restart
```

## Expected Behavior

When you visit `https://apps.kuracodez.space/krypto-dashboard/app`:

1. ✅ Nginx receives request at `/krypto-dashboard/app`
2. ✅ Proxy forwards to `http://127.0.0.1:5013/krypto-dashboard/app`
3. ✅ Panel serves the Cryptocurrency Dashboard Hub
4. ✅ WebSocket connection established for interactivity
5. ✅ Dashboard sidebar and main content displayed

## Files Structure

```
/home/kuranez/Projects/GitHub/krypto-dashboard-web/
├── docker-compose.yml          # Production (pulls from GHCR)
├── docker-compose.build.yml    # Development (builds locally)
├── Dockerfile                  # Container definition
├── keys.env                    # API keys (gitignored, not committed)
├── keys.env.example           # Template for keys.env
└── web/
    ├── app/
    │   ├── launch.py          # Entry point with /krypto-dashboard/app path
    │   ├── main.py            # App creation
    │   └── ...
    ├── dashboards/            # Dashboard modules
    └── assets/                # Static files
```

## Troubleshooting

### If app doesn't load:

1. **Check container is running:**
   ```bash
   docker ps | grep krypto
   ```

2. **Test direct access:**
   ```bash
   curl http://127.0.0.1:5013/krypto-dashboard/app
   ```

3. **Check logs for errors:**
   ```bash
   docker logs krypto-dashboard-web_krypto-dashboard-web_1
   ```

4. **Verify nginx config in Plesk**
   - Ensure the location block exists
   - Check for typos in the path

### If you see blank page:

- Check browser console (F12) for JavaScript errors
- Verify WebSocket connection is established
- Ensure `/app` is in the URL: `https://apps.kuracodez.space/krypto-dashboard/app`

## Updates

To update the app:

1. **Pull latest code:**
   ```bash
   cd /home/kuranez/Projects/GitHub/krypto-dashboard-web
   git pull origin main
   ```

2. **Rebuild image:**
   ```bash
   docker build -t ghcr.io/kuranez/krypto-dashboard-web:latest .
   ```

3. **Restart container:**
   ```bash
   docker-compose down && docker-compose up -d
   ```

4. **(Optional) Push to GHCR:**
   ```bash
   docker push ghcr.io/kuranez/krypto-dashboard-web:latest
   ```

## Status: ✅ READY FOR PRODUCTION

The app is configured correctly and should work at:
**https://apps.kuracodez.space/krypto-dashboard/app**
