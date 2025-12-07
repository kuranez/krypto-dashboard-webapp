"""
Pytest tests to verify the correlation and beta calculations work correctly.
"""
import pytest
import pandas as pd
from data_manager import DataManager


@pytest.fixture
def data_manager():
    """Create a DataManager instance for testing."""
    return DataManager()


@pytest.fixture
def btc_data(data_manager):
    """Fetch BTC data for testing."""
    df = data_manager.fetch_combined_data('BTCUSDT')
    assert not df.empty, "Failed to fetch BTC data"
    return df


@pytest.fixture
def eth_data(data_manager):
    """Fetch ETH data for testing."""
    df = data_manager.fetch_combined_data('ETHUSDT')
    assert not df.empty, "Failed to fetch ETH data"
    return df


class TestCorrelationBeta:
    """Test suite for correlation and beta calculations."""
    
    def test_fetch_btc_data(self, btc_data):
        """Test that BTC data can be fetched."""
        assert isinstance(btc_data, pd.DataFrame)
        assert len(btc_data) > 0
        print(f"\n   ✓ BTC: {len(btc_data)} data points")
    
    def test_fetch_eth_data(self, eth_data):
        """Test that ETH data can be fetched."""
        assert isinstance(eth_data, pd.DataFrame)
        assert len(eth_data) > 0
        print(f"\n   ✓ ETH: {len(eth_data)} data points")
    
    def test_rolling_correlation(self, data_manager, eth_data, btc_data):
        """Test rolling correlation calculation."""
        window = 30
        corr_series = data_manager.calculate_rolling_correlation(eth_data, btc_data, window=window)
        
        assert isinstance(corr_series, pd.Series)
        assert len(corr_series) > 0
        assert not corr_series.empty
        
        latest_corr = corr_series.iloc[-1]
        assert -1 <= latest_corr <= 1, "Correlation must be between -1 and 1"
        
        print(f"\n   ✓ Correlation series: {len(corr_series)} values")
        print(f"   ✓ Latest correlation: {latest_corr:.4f}")
    
    def test_rolling_beta(self, data_manager, eth_data, btc_data):
        """Test rolling beta coefficient calculation."""
        window = 30
        beta_series = data_manager.calculate_beta_coefficient(eth_data, btc_data, window=window)
        
        assert isinstance(beta_series, pd.Series)
        assert len(beta_series) > 0
        assert not beta_series.empty
        
        latest_beta = beta_series.iloc[-1]
        assert latest_beta > 0, "Beta should be positive for positively correlated assets"
        
        print(f"\n   ✓ Beta series: {len(beta_series)} values")
        print(f"   ✓ Latest beta: {latest_beta:.4f}")
    
    def test_get_latest_correlation_beta(self, data_manager, eth_data, btc_data):
        """Test the helper method that returns both correlation and beta."""
        window = 30
        correlation, beta = data_manager.get_latest_correlation_beta(eth_data, btc_data, window=window)
        
        assert isinstance(correlation, (float, int))
        assert isinstance(beta, (float, int))
        assert -1 <= correlation <= 1, "Correlation must be between -1 and 1"
        assert beta > 0, "Beta should be positive for positively correlated assets"
        
        print(f"\n   ✓ Correlation: {correlation:.4f}")
        print(f"   ✓ Beta: {beta:.4f}")
        
        # Print interpretation
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
