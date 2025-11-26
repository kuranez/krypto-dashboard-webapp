#!/usr/bin/env python3
"""
Simple test launcher for the dashboard
"""

import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def launch_simple():
    """Launch just the simple dashboard for testing."""
    import panel as pn
    
    # Configure Panel
    pn.extension('plotly')
    
    # Import and create the simple dashboard
    sys.path.append(str(Path(__file__).parent / "dashboards"))
    from simple_price_dashboard import SimplePriceDashboard
    
    # Create dashboard instance
    dashboard = SimplePriceDashboard()
    
    # Create the layout
    layout = dashboard.create_dashboard()
    
    # Serve the dashboard
    print("🚀 Starting Simple Price Dashboard...")
    print("📊 Dashboard will open in your browser")
    print("🔗 URL: http://localhost:5006")
    print("⏹️  Press Ctrl+C to stop")
    
    layout.servable()
    layout.show(port=5006)

if __name__ == "__main__":
    launch_simple()
