# Operations: Run & Deploy

## Local Development
- Dev runner: `web/app/launch.py` (adds app + web root to `sys.path`, port fallback)
- Serve via Panel:
  ```bash
  panel serve web/app/main.py --autoreload --dev
  ```
- Direct show:
  ```bash
  /home/kuranez/miniconda3/envs/jupyter_env/bin/python web/app/launch.py
  ```

## Docker
- Build:
  ```bash
  docker build -t ghcr.io/kuranez/krypto-dashboard-web:latest .
  ```
- Push:
  ```bash
  docker push ghcr.io/kuranez/krypto-dashboard-web:latest
  ```
- Compose:
  ```bash
  docker-compose up -d
  ```

## Environment & Requirements
- Python deps: `web/requirements.txt`
- Testing deps: `testing/requirements.txt`
- Conda env: `jupyter_env`
