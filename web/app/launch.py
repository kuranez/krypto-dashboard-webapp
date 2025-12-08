#!/usr/bin/env python3
"""
Launch script for local development of the Cryptocurrency Dashboard App
For production deployment, use: panel serve main.py --prefix /krypto-dashboard
"""

import sys
from pathlib import Path

# Add the current app directory and the web root to Python path
current_dir = Path(__file__).parent
web_root = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(web_root))

def main():
    """Launch the dashboard application for local development."""
    try:
        from main import app
        
        print("🚀 Starting Cryptocurrency Dashboard (Development mode)...")
        print("📊 Dashboard will open in your default browser")
        print("🔗 Access URL: http://localhost:5007")
        print("⏹️  Press Ctrl+C to stop the server")
        
        # Try default port, then fallback automatically to 5008
        for port in (5007, 5008):
            try:
                print(f"🔌 Attempting to start on port {port}...")
                app.show(port=port, autoreload=True)
                break
            except OSError as e:
                if "Address already in use" in str(e):
                    print(f"\n⚠️  Port {port} is already in use! Trying next...")
                    continue
                raise
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("💡 Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
