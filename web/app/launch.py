#!/usr/bin/env python3
"""
Launch script for local development of the Cryptocurrency Dashboard App
For production deployment, use: panel serve main.py --prefix /krypto-dashboard
"""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Launch the dashboard application for local development."""
    try:
        from main import app
        
        print("🚀 Starting Cryptocurrency Dashboard (Development mode)...")
        print("📊 Dashboard will open in your default browser")
        print("🔗 Access URL: http://localhost:5007")
        print("⏹️  Press Ctrl+C to stop the server")
        
        try:
            app.show(port=5007, autoreload=True)
        except OSError as e:
            if "Address already in use" in str(e):
                print("\n⚠️  Port 5007 is already in use!")
                print("💡 Either:")
                print("   1. Stop the existing server (Ctrl+C in that terminal)")
                print("   2. Or use a different port:")
                print("      python -c \"import sys; sys.path.insert(0, 'app'); from main import app; app.show(port=5008)\"")
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
