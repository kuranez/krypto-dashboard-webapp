# Proxy entrypoint for Panel/Bokeh server
# Allows: panel serve main.py --prefix /krypto-dashboard

from web.app.main import app as app

# Optional: expose a doc if needed by certain runners
try:
    doc = app._documents[0] if getattr(app, "_documents", None) else None
except Exception:
    doc = None
