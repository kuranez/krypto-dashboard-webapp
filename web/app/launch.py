#!/usr/bin/env python3
"""
Launch script for the Cryptocurrency Dashboard App
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Launch the dashboard application."""
    try:
        from main import create_app
        
        # Detect if running in Docker
        in_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER')
        
        # Create the app
        app = create_app()
        
        if in_docker:
            # Docker/production mode: use pn.serve for proper deployment
            import panel as pn
            print("🚀 Starting Cryptocurrency Dashboard (Docker mode)...")
            print("📊 Server running on port 5013")
            print("🔗 Access at: http://0.0.0.0:5013")
            print("⏹️  Press Ctrl+C to stop the server")
            
            pn.serve(
                app,
                address='0.0.0.0',
                port=5013,
                allow_websocket_origin=['*'],  # Allow all origins (use reverse proxy for security)
                show=False,
                num_procs=1,
                websocket_max_message_size=100*1024*1024,
                static_dirs={'assets': str(Path(__file__).parent.parent / 'assets')}
            )
        else:
            # Local development mode: use show for auto-opening browser
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
                    print("      python -c \"import sys; sys.path.insert(0, 'app'); from main import create_app; create_app().show(port=5008)\"")
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
