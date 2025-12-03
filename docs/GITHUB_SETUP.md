# GitHub Repository and GHCR Setup Guide

This guide will help you publish this project to GitHub and set up automated Docker image publishing to GitHub Container Registry (GHCR).

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository:
   - **Repository name**: `krypto-dashboard-web`
   - **Description**: "Modular cryptocurrency dashboard built with HoloViz Panel"
   - **Visibility**: Choose Public or Private
   - **Don't initialize** with README (we already have one)

## Step 2: Initialize Git and Push

```bash
# Initialize git repository (if not already done)
cd /home/kuranez/Projects/GitHub/krypto-dashboard-web
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Cryptocurrency Dashboard Web"

# Add remote repository (replace 'kuranez' with your GitHub username)
git remote add origin https://github.com/kuranez/krypto-dashboard-web.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Container Registry

GHCR is automatically available for all GitHub repositories. The GitHub Actions workflow will handle publishing.

### Make Package Public (Optional)

After the first Docker image is pushed:

1. Go to your GitHub profile → Packages
2. Find `krypto-dashboard-web` package
3. Click on the package
4. Go to "Package settings" (right sidebar)
5. Scroll to "Danger Zone"
6. Click "Change visibility" → Select "Public"
7. Confirm the change

## Step 4: Verify GitHub Actions Workflow

The workflow is already created at `.github/workflows/docker-publish.yml`

**It will automatically:**
- Build Docker image on every push to `main` branch
- Tag images with `latest` for main branch
- Support semantic versioning for tagged releases
- Use GitHub Actions cache for faster builds
- Build for both AMD64 and ARM64 platforms

### Trigger First Build

The workflow will run automatically when you push to `main`:

```bash
git push origin main
```

Monitor the build:
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Watch the "Build and Publish Docker Image" workflow

## Step 5: Pull and Use Your Published Image

Once the workflow completes successfully:

```bash
# Pull the image
docker pull ghcr.io/kuranez/krypto-dashboard-web:latest

# Run the container
docker run -p 5013:5013 ghcr.io/kuranez/krypto-dashboard-web:latest

# Or use docker-compose
docker-compose up
```

## Step 6: Create Release (Optional)

For versioned releases:

```bash
# Tag your release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This will create additional Docker tags:
- `ghcr.io/kuranez/krypto-dashboard-web:1.0.0`
- `ghcr.io/kuranez/krypto-dashboard-web:1.0`
- `ghcr.io/kuranez/krypto-dashboard-web:1`
- `ghcr.io/kuranez/krypto-dashboard-web:latest`

## Automated Publishing

The GitHub Actions workflow handles everything:
- ✅ Automatic builds on push to main
- ✅ Multi-platform support (AMD64, ARM64)
- ✅ Build caching for speed
- ✅ Semantic versioning
- ✅ No manual Docker login needed (uses GITHUB_TOKEN)

## Environment Variables

To use with API keys:

```bash
# Create .env file locally
echo "BINANCE_API_KEY=your_key_here" > .env

# Run with docker-compose (reads .env automatically)
docker-compose up

# Or pass directly
docker run -p 5013:5013 -e BINANCE_API_KEY=your_key ghcr.io/kuranez/krypto-dashboard-web:latest
```

## Troubleshooting

### Workflow Fails
- Check Actions tab for error logs
- Ensure repository has Actions enabled (Settings → Actions → General)
- Verify Dockerfile builds locally: `docker build -t test .`

### Package Not Visible
- Make package public in Package settings
- Check if workflow completed successfully

### Cannot Pull Image
- Ensure package is public, or
- Authenticate: `echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin`

## Badge for README (Optional)

Add this to your README.md to show build status:

```markdown
[![Docker Image](https://github.com/kuranez/krypto-dashboard-web/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/kuranez/krypto-dashboard-web/actions/workflows/docker-publish.yml)
```

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Wait for first build to complete
3. ✅ Make package public (if desired)
4. ✅ Test pulling and running the image
5. ✅ Create your first release tag (optional)

For more information, visit:
- [GitHub Packages Documentation](https://docs.github.com/en/packages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
