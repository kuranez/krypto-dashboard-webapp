# Troubleshooting 404 and Blank Pages

## Current Status ✅

- **Container**: Running correctly on port 5013
- **Direct access**: `http://127.0.0.1:5013/` returns HTTP 200 with full HTML
- **App serves**: Cryptocurrency Dashboard Hub at root path `/`

## Problem: 404 and Blank Pages via Reverse Proxy

### Symptoms:
- `https://apps.kuracodez.space/krypto-dashboard` → 404
- `https://apps.kuracodez.space/krypto-dashboard/main` → Blank page

### Root Cause:
The reverse proxy configuration in Plesk is either:
1. Missing
2. Incorrect
3. Not applied/reloaded

## Solution: Configure Nginx Reverse Proxy in Plesk

### Step-by-Step Instructions:

1. **Login to Plesk**
   - Navigate to your Plesk control panel

2. **Go to Domain Settings**
   - Domains → `apps.kuracodez.space`

3. **Open Apache & Nginx Settings**
   - Click on "Apache & Nginx Settings"

4. **Add Nginx Directives**
   - Scroll to "Additional nginx directives" section
   - **Copy and paste this EXACTLY:**

```nginx
location = /krypto-dashboard {
    return 301 /krypto-dashboard/;
}

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
```

5. **Save Configuration**
   - Click "OK" or "Apply" button
   - Plesk will automatically reload nginx

6. **Test Access**
   - Visit: `https://apps.kuracodez.space/krypto-dashboard`
   - Should redirect to: `https://apps.kuracodez.space/krypto-dashboard/`
   - Dashboard should load

## Verification Steps

### From the Server (SSH):

```bash
# 1. Check if container is running
docker ps | grep krypto-dashboard-web

# 2. Test direct access
curl -I http://127.0.0.1:5013/

# 3. Run diagnostic script
./test-proxy.sh
```

### From Browser:

1. Open Developer Tools (F12)
2. Go to Network tab
3. Visit `https://apps.kuracodez.space/krypto-dashboard`
4. Check for:
   - **200 responses** (good)
   - **404 responses** (bad - proxy not working)
   - **403 websocket errors** (check websocket headers)

## Common Issues

### Issue 1: Still Getting 404

**Possible causes:**
- Nginx directives not saved correctly
- Nginx not reloaded
- Conflicting location blocks

**Solution:**
```bash
# Check nginx config syntax
nginx -t

# Reload nginx manually
systemctl reload nginx
# OR (in Plesk)
service nginx reload
```

### Issue 2: Blank Page (No 404)

**Possible causes:**
- WebSocket connection failing
- Static files not loading
- CORS issues

**Check browser console for errors:**
- Press F12
- Look for red errors
- Common: "WebSocket connection failed"

**Solution:** Ensure the `Upgrade` and `Connection` headers are set in nginx config (they are in the config above).

### Issue 3: Works Directly but Not Through Proxy

**This means:**
- Container is fine ✅
- Proxy configuration is wrong ❌

**Solution:**
1. Double-check the nginx directives in Plesk
2. Make sure there's a trailing `/` in `proxy_pass http://127.0.0.1:5013/;`
3. Ensure no typos in the location path

### Issue 4: `/krypto-dashboard/main` Shows Blank

**This is expected behavior!** The app doesn't have a `/main` route.

**Correct URLs:**
- ✅ `https://apps.kuracodez.space/krypto-dashboard/` (root of app)
- ❌ `https://apps.kuracodez.space/krypto-dashboard/main` (doesn't exist)

The app serves everything from its root. Panel will handle routing internally.

## Understanding the URL Structure

```
Browser Request:
https://apps.kuracodez.space/krypto-dashboard/
                                    ↓
Nginx receives: /krypto-dashboard/
                                    ↓
Nginx config: location /krypto-dashboard/ { proxy_pass http://127.0.0.1:5013/; }
                                    ↓
Strips prefix, forwards: /
                                    ↓
Container receives: /
                                    ↓
Panel serves: Dashboard Hub
```

## Alternative: Access Without Reverse Proxy

**For testing purposes only:**

If you open port 5013 in the firewall:
```bash
# Open firewall (temporary)
ufw allow 5013/tcp

# Access directly
http://apps.kuracodez.space:5013/
```

**Not recommended for production!** Always use reverse proxy with SSL.

## Expected Behavior After Fix

1. Visit: `https://apps.kuracodez.space/krypto-dashboard`
2. Auto-redirect to: `https://apps.kuracodez.space/krypto-dashboard/`
3. See: **Cryptocurrency Dashboard Hub** page
4. Left sidebar: Logo and dashboard selector
5. Main area: Welcome message or selected dashboard
6. No console errors
7. WebSocket connected (check Network tab → WS)

## Still Not Working?

### Check Plesk Logs:

```bash
# Nginx error log
tail -f /var/log/nginx/error.log

# Nginx access log
tail -f /var/log/nginx/access.log

# Docker container log
docker logs -f krypto-dashboard-web_krypto-dashboard-web_1
```

### Verify Nginx Config Location:

Plesk might use different config files:
```bash
# Find nginx config for your domain
grep -r "apps.kuracodez.space" /etc/nginx/

# Check if your directives are there
grep -r "krypto-dashboard" /etc/nginx/
```

### Contact Support:

If none of this works, the issue might be:
- Plesk-specific configuration
- Custom nginx setup
- Conflicting proxy rules

Share:
1. Plesk version
2. Output of `nginx -V`
3. Content of nginx config for the domain
4. Browser console errors (screenshot)
