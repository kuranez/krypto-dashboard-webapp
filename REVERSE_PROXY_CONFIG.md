# Reverse Proxy Configuration for Plesk

The Docker container now runs on port 5013 **without** a URL prefix. You need to configure your reverse proxy to handle the `/krypto-dashboard` prefix.

## What Changed

**Before (broken):**
- App served at: `http://0.0.0.0:5013/krypto-dashboard`
- Static files had 404 errors due to prefix issues

**Now (working):**
- App serves at: `http://0.0.0.0:5013/` (root)
- Reverse proxy adds the `/krypto-dashboard` prefix
- All static files and websockets work correctly

## Nginx Configuration for Plesk

### Option 1: Using Plesk Nginx Additional Directives

1. Go to **Plesk → Domains → apps.kuracodez.space → Apache & Nginx Settings**
2. Add to **Additional nginx directives**:

```nginx
location /krypto-dashboard/ {
    proxy_pass http://127.0.0.1:5013/;
    proxy_http_version 1.1;
    
    # WebSocket support
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    
    # Standard proxy headers
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Port $server_port;
    
    # Timeouts for long-running connections
    proxy_connect_timeout 7d;
    proxy_send_timeout 7d;
    proxy_read_timeout 7d;
}
```

### Option 2: Direct Nginx Config File

If you have access to nginx config files directly:

```nginx
server {
    listen 80;
    server_name apps.kuracodez.space;
    
    location /krypto-dashboard/ {
        proxy_pass http://127.0.0.1:5013/;
        proxy_http_version 1.1;
        
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

## Apache Configuration (Alternative)

If using Apache instead of Nginx:

```apache
<Location /krypto-dashboard>
    ProxyPass http://127.0.0.1:5013/
    ProxyPassReverse http://127.0.0.1:5013/
    
    # WebSocket support
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} =websocket [NC]
    RewriteRule /krypto-dashboard/(.*) ws://127.0.0.1:5013/$1 [P,L]
    
    # Headers
    RequestHeader set X-Forwarded-Proto "https"
    RequestHeader set X-Forwarded-Port "443"
</Location>
```

Required Apache modules:
```bash
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel
a2enmod headers
a2enmod rewrite
systemctl restart apache2
```

## Testing

After configuring the reverse proxy:

1. **Access the app**: https://apps.kuracodez.space/krypto-dashboard
2. **Check browser console** for any errors
3. **Verify WebSocket**: Should see WebSocket connection established (not 403 errors)

## Troubleshooting

### White Page / No Content

**Check:**
```bash
# Verify container is running
docker ps | grep krypto

# Check logs for errors
docker logs krypto-dashboard-web_krypto-dashboard-web_1

# Test direct access (from server)
curl http://127.0.0.1:5013/
```

### WebSocket 403 Errors

**Solution:** Make sure `proxy_set_header Upgrade` and `Connection "upgrade"` are set in nginx config.

### Static Files 404

**Solution:** Ensure the trailing slash in `proxy_pass http://127.0.0.1:5013/;` - it's critical!

### Connection Timeout

**Solution:** Increase timeout values in nginx config (already set to 7 days in example above).

## Direct Access (Without Reverse Proxy)

For testing, you can access directly:
- **From server**: http://127.0.0.1:5013
- **From outside** (if firewall allows): http://apps.kuracodez.space:5013

But for production, use the reverse proxy with HTTPS.

## SSL/HTTPS

Plesk should handle SSL automatically. The reverse proxy will:
- Receive HTTPS requests on port 443
- Forward to Docker container on HTTP port 5013
- Docker doesn't need SSL (reverse proxy terminates SSL)

## Summary

1. ✅ Docker container runs on `http://127.0.0.1:5013/` (no prefix)
2. ✅ Reverse proxy adds `/krypto-dashboard` prefix
3. ✅ WebSocket connections work properly
4. ✅ Static files load correctly
5. ✅ SSL terminated at reverse proxy level
