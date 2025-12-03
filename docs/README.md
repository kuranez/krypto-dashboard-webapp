# Documentation

## Quick Start

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common commands for development and deployment

## Deployment

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide for local, Docker, and Plesk
- **[GITHUB_CONTAINER_REGISTRY.md](GITHUB_CONTAINER_REGISTRY.md)** - Guide for pushing/pulling Docker images to GHCR

## Current Setup

**App serves at:** `http://0.0.0.0:5013/krypto-dashboard`  
**Production URL:** `https://apps.kuracodez.space/krypto-dashboard`

The container runs on port 5013, and nginx in Plesk forwards `/krypto-dashboard/` to the container.
