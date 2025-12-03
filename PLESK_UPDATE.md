# Plesk Server Update Instructions

## Problem
Plesk is using the old image from GHCR that still serves at `/krypto-dashboard/main` instead of `/krypto-dashboard/app`.

## Solution: Use docker-compose.build.yml

In Plesk, change the configuration file from `docker-compose.yml` to `docker-compose.build.yml`.

### Steps in Plesk:

1. **Go to Docker Extension**
   - Docker → Stacks → krypto-dashboard-web

2. **Edit Stack Settings**
   - Click on the stack name or "Edit" button

3. **Change Compose File**
   - **Current:** `docker-compose.yml` (pulls from GHCR)
   - **Change to:** `docker-compose.build.yml` (builds locally)

4. **Redeploy**
   - Click "Redeploy" or "Update"
   - Plesk will build the image from source on the server
   - This will use the latest code with `/krypto-dashboard/app`

### Alternative: Manual Command on Server

If you have SSH access to the Plesk server:

```bash
# Navigate to the repository
cd /var/www/vhosts/kuracodez.space/apps.kuracodez.space/repos/krypto-dashboard-web/

# Pull latest code
git pull origin main

# Build and restart with build config
docker-compose -f docker-compose.build.yml down
docker-compose -f docker-compose.build.yml up -d --build

# Verify it's running
docker logs krypto-dashboard-web-krypto-dashboard-web-1

# You should see:
# Bokeh app running at: http://0.0.0.0:5013/krypto-dashboard/app
```

### Verify the Fix

After redeploying, check the logs in Plesk console. You should see:

**Before (old):**
```
Bokeh app running at: http://0.0.0.0:5013/krypto-dashboard/main
```

**After (fixed):**
```
🚀 Starting Cryptocurrency Dashboard (Docker mode)...
🔗 Access at: http://0.0.0.0:5013/krypto-dashboard/app
```

Then access: `https://apps.kuracodez.space/krypto-dashboard/app`

## Why This Happened

- `docker-compose.yml` pulls the pre-built image from GHCR
- GHCR has the old version (before the `/app` fix)
- `docker-compose.build.yml` builds from the latest source code
- Since you can't push to GHCR from your local machine, use the build config

## Future: Automatic Updates via GitHub Actions

To avoid this in the future, GitHub Actions can automatically build and push to GHCR when you push code. The workflow is already set up at `.github/workflows/docker-publish.yml` but it needs GHCR to be accessible.

For now, use `docker-compose.build.yml` on the Plesk server.
