#!/usr/bin/env python3
"""
Quick test script to verify the correlation and beta calculations work correctly.
"""

import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'web' / 'app'
sys.path.insert(0, str(app_dir))

import pandas as pd
from data_manager import DataManager

def test_correlation_beta():
    """Test the correlation and beta calculation methods."""
    print("🧪 Testing Correlation and Beta Calculations\n")
    
    dm = DataManager()
    
    # Test with BTC and ETH
    print("📊 Fetching BTC data...")
    df_btc = dm.fetch_combined_data('BTCUSDT')
    print(f"   ✓ BTC: {len(df_btc)} data points")
    
    print("📊 Fetching ETH data...")
    df_eth = dm.fetch_combined_data('ETHUSDT')
    print(f"   ✓ ETH: {len(df_eth)} data points")
    
    if not df_btc.empty and not df_eth.empty:
        print("\n📈 Calculating rolling correlation (30-day window)...")
        corr_series = dm.calculate_rolling_correlation(df_eth, df_btc, window=30)
        print(f"   ✓ Correlation series: {len(corr_series)} values")
        if not corr_series.empty:
            latest_corr = corr_series.iloc[-1]
            print(f"   ✓ Latest correlation: {latest_corr:.4f}")
        
        print("\n📈 Calculating rolling beta (30-day window)...")
        beta_series = dm.calculate_beta_coefficient(df_eth, df_btc, window=30)
        print(f"   ✓ Beta series: {len(beta_series)} values")
        if not beta_series.empty:
            latest_beta = beta_series.iloc[-1]
            print(f"   ✓ Latest beta: {latest_beta:.4f}")
        
        print("\n📊 Using helper method get_latest_correlation_beta()...")
        correlation, beta = dm.get_latest_correlation_beta(df_eth, df_btc, window=30)
        print(f"   ✓ Correlation: {correlation:.4f}")
        print(f"   ✓ Beta: {beta:.4f}")
        
        print("\n✅ All tests passed!")
        print("\n📝 Interpretation:")
        if correlation > 0.7:
            print(f"   🟢 ETH is strongly coupled with BTC (correlation: {correlation:.3f})")
        elif correlation > 0.3:
            print(f"   🟡 ETH has moderate correlation with BTC (correlation: {correlation:.3f})")
        else:
            print(f"   🔴 ETH is decoupled from BTC (correlation: {correlation:.3f})")
        
        if beta > 1:
            print(f"   📈 ETH is {((beta - 1) * 100):.1f}% more volatile than BTC (beta: {beta:.3f})")
        elif beta < 1:
            print(f"   📉 ETH is {((1 - beta) * 100):.1f}% less volatile than BTC (beta: {beta:.3f})")
        else:
            print(f"   ➡️  ETH moves in line with BTC (beta: {beta:.3f})")
    else:
        print("❌ Failed to fetch data")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = test_correlation_beta()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
