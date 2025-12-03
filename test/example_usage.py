#!/usr/bin/env python3
"""
Example: Creating a simple price chart using the modular components
"""

import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def example_usage():
    """Show how to use the modular components."""
    print("📊 Creating a simple price chart using modular components...\n")
    
    # Import the components
    from data_manager import DataManager
    from figure_factory import FigureFactory
    from config import AppConfig
    
    # Create instances
    config = AppConfig()
    data_manager = DataManager()
    figure_factory = FigureFactory()
    
    print("✅ Components created")
    
    # Fetch some data
    print("🔄 Fetching BTC data...")
    df = data_manager.fetch_historical_data('BTCUSDT', limit=100)
    
    if not df.empty:
        print(f"✅ Fetched {len(df)} data points")
        
        # Create a chart
        print("📈 Creating price chart...")
        fig = figure_factory.create_simple_price_chart(df, 'BTC', 'Bitcoin Price Chart')
        
        print("✅ Chart created successfully!")
        print(f"   - Chart has {len(fig.data)} traces")
        print(f"   - Chart title: {fig.layout.title.text}")
        
        # Show available colors
        btc_primary = config.get_crypto_color('BTC', 'primary')
        btc_secondary = config.get_crypto_color('BTC', 'secondary')
        print(f"   - BTC colors: {btc_primary} (primary), {btc_secondary} (secondary)")
        
    else:
        print("❌ No data fetched - check your internet connection")
    
    print("\n🎉 Example completed successfully!")
    print("💡 The modular components are working and ready to use!")

if __name__ == "__main__":
    example_usage()
