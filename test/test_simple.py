#!/usr/bin/env python3
"""
Quick test for the simple dashboard
"""

import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def test_simple_dashboard():
    """Test the simple dashboard creation."""
    print("🧪 Testing Simple Dashboard...")
    
    try:
        from dashboard_registry import DashboardRegistry
        
        registry = DashboardRegistry()
        registry.discover_dashboards()
        
        dashboards = registry.get_available_dashboards()
        print(f"✅ Found {len(dashboards)} dashboards:")
        for name in dashboards.keys():
            print(f"   - {name}")
        
        # Test creating a simple dashboard instance
        if "Simple Price Chart" in dashboards:
            dashboard_class = dashboards["Simple Price Chart"]
            dashboard = dashboard_class()
            print(f"✅ Created Simple Price Dashboard instance")
            
            # Test creating the layout (but don't display it)
            layout = dashboard.create_dashboard()
            print(f"✅ Dashboard layout created successfully")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Testing Simple Dashboard App\n")
    
    if test_simple_dashboard():
        print("\n🎉 Simple dashboard test passed!")
        print("💡 Run 'python launch.py' to start the app")
    else:
        print("\n❌ Dashboard test failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
