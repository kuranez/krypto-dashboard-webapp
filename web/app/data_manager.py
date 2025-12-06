"""
Data Manager
Handles data fetching, caching, and processing for dashboards.
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import panel as pn
from config import AppConfig

class DataManager:
    """Manages data fetching and caching for cryptocurrency data."""
    
    def __init__(self):
        self.config = AppConfig()
        self._setup_api()
        
    def _setup_api(self):
        """Setup API configuration."""
        # Try to load from multiple possible locations
        env_paths = [
            'keys.env',
            '../keys.env',
            '../../keys.env'
        ]
        
        for path in env_paths:
            if os.path.exists(path):
                load_dotenv(path)
                break
        
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.base_url = 'https://api.binance.us/api/v3'
        self.klines_url = f'{self.base_url}/klines'
        self.price_url = f'{self.base_url}/ticker/price'
    
    @pn.cache
    def fetch_historical_data(self, 
                             symbol: str = 'BTCUSDT', 
                             interval: str = '1h',  # Changed from '1d' to '1h' for more data points
                             start_time: Optional[int] = None, 
                             end_time: Optional[int] = None, 
                             limit: int = 1000) -> pd.DataFrame:  # Binance max is 1000
        """Fetch historical data for a given symbol from Binance API."""
        
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
            
        headers = {}
        if self.api_key:
            headers['X-MBX-APIKEY'] = self.api_key
        
        try:
            response = requests.get(
                self.klines_url, 
                headers=headers, 
                params=params,
                timeout=self.config.api_config['timeout']
            )
            
            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
                return pd.DataFrame()

            data = response.json()
            df = pd.DataFrame(data, columns=[
                'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
                'Close Time', 'Quote Asset Volume', 'Number of Trades',
                'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
            ])
            
            # Process the data
            df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')
            df = df.drop(columns=[
                'Open Time', 'Close Time', 'Quote Asset Volume',
                'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
            ])
            
            # Convert price columns to float
            price_columns = ['Open', 'High', 'Low', 'Close']
            for col in price_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
            df['Symbol'] = symbol[:-4] if symbol.endswith('USDT') else symbol
            
            return df
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    @pn.cache
    def fetch_current_price(self, symbol: str) -> float:
        """Fetch the current price for a given symbol from Binance API."""
        
        try:
            response = requests.get(
                f"{self.price_url}?symbol={symbol}",
                timeout=self.config.api_config['timeout']
            )
            
            if response.status_code == 200:
                data = response.json()
                return float(data.get('price', 0))
            else:
                print(f"Error fetching current price for {symbol}: {response.status_code}")
                return 0.0
                
        except Exception as e:
            print(f"Error fetching current price for {symbol}: {e}")
            return 0.0
    
    def fetch_smart_data(self, symbol: str, time_period: str = '1Y') -> pd.DataFrame:
        """Fetch historical data with smart interval selection based on time period.
        
        Uses different intervals based on time period:
        - Short periods (< 6M): hourly data (1h)
        - Medium periods (6M-3Y): daily data (1d)
        - Long periods (5Y, All_Time): weekly data (1w)
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            time_period: Time period from config (e.g., '1W', '1M', '1Y', '5Y', 'All_Time')
        
        Returns:
            DataFrame with historical price data
        """
        period_config = self.config.time_intervals.get(time_period, {})
        days = period_config.get('days', 365)
        
        # For All_Time or very long periods (5Y+), use weekly data
        if days == 'max' or days >= 5*365:
            # Use weekly data (1w interval gives ~1000 weeks ~ 19 years)
            df = self.fetch_historical_data(symbol=symbol, interval='1w', limit=1000)
            return df
        
        # For long periods (1Y - 3Y), use daily data
        elif days > 180:
            # Use daily data
            limit = min(days, 1000)
            df = self.fetch_historical_data(symbol=symbol, interval='1d', limit=limit)
            return df
        
        # For short periods (< 6M), use hourly data
        else:
            # Use hourly data (up to 1000 hours ~ 41 days)
            df = self.fetch_historical_data(symbol=symbol, interval='1h', limit=1000)
            return df
    
    def fetch_combined_data(self, symbol: str) -> pd.DataFrame:
        """Fetch multi-timeframe data and combine them intelligently.
        
        Fetches three timeframes for comprehensive coverage:
        - Weekly data: 1000 weeks (~19 years) for long-term history
        - Daily data: 1000 days (~2.7 years) for medium-term
        - Hourly data: 1000 hours (~41 days) for recent high-resolution
        
        Combines them without overlap for optimal chart performance.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
        
        Returns:
            DataFrame with combined historical price data across all timeframes
        """
        try:
            # Fetch hourly data for recent period (1000 hours ~ 41 days)
            df_hourly = self.fetch_historical_data(symbol=symbol, interval='1h', limit=1000)
            
            # Fetch daily data for medium-term history (1000 days ~ 2.7 years)
            df_daily = self.fetch_historical_data(symbol=symbol, interval='1d', limit=1000)
            
            # Fetch weekly data for long-term history (1000 weeks ~ 19 years)
            df_weekly = self.fetch_historical_data(symbol=symbol, interval='1w', limit=1000)
            
            # Handle empty data cases
            if df_hourly.empty and df_daily.empty and df_weekly.empty:
                return pd.DataFrame()
            
            # Start with weekly data as the base
            combined = df_weekly.copy() if not df_weekly.empty else pd.DataFrame()
            
            # Add daily data (excluding overlap with hourly)
            if not df_daily.empty:
                if not df_hourly.empty:
                    hourly_start = df_hourly['Date'].min()
                    df_daily_filtered = df_daily[df_daily['Date'] < hourly_start].copy()
                else:
                    df_daily_filtered = df_daily.copy()
                
                # Remove daily data that overlaps with weekly
                if not combined.empty:
                    daily_start = df_daily_filtered['Date'].min()
                    combined = combined[combined['Date'] < daily_start].copy()
                
                if not df_daily_filtered.empty:
                    combined = pd.concat([combined, df_daily_filtered], ignore_index=True)
            
            # Add hourly data (most recent, no overlap)
            if not df_hourly.empty:
                combined = pd.concat([combined, df_hourly], ignore_index=True)
            
            # Sort and clean
            if not combined.empty:
                combined = combined.sort_values('Date').reset_index(drop=True)
                # Remove any duplicate dates (keep last which is more granular)
                combined = combined.drop_duplicates(subset=['Date'], keep='last').reset_index(drop=True)
            
            return combined
                
        except Exception as e:
            print(f"Error fetching combined data for {symbol}: {e}")
            return pd.DataFrame()
    
    def add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicators (SMAs and EMAs) to the DataFrame.
        
        This is the single source of truth for all moving average calculations.
        """
        if df.empty:
            return df
            
        df = df.copy()
        # Simple Moving Averages
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        # Exponential Moving Averages
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
        
        return df
    
    def add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Deprecated: Use add_technical_indicators() instead."""
        return self.add_technical_indicators(df)
    
    def filter_outliers_percentiles(self, df: pd.DataFrame, column_name: str, 
                                   lower_percentile: float = 0.01, 
                                   upper_percentile: float = 99.99) -> pd.DataFrame:
        """Filter outliers from a DataFrame column using percentile-based bounds.
        
        This method removes extreme outliers by filtering values outside the specified
        percentile range. Useful for cleaning data before visualization or analysis.
        
        Args:
            df: DataFrame to filter
            column_name: Name of the column to filter on
            lower_percentile: Lower percentile threshold (default: 0.01 = bottom 0.01%)
            upper_percentile: Upper percentile threshold (default: 99.99 = top 99.99%)
        
        Returns:
            Filtered DataFrame with outliers removed
            
        Example:
            # Remove extreme volume outliers
            clean_df = data_manager.filter_outliers_percentiles(df, 'Volume', 1.0, 99.0)
        """
        if df.empty or column_name not in df.columns:
            return df
        
        lower_bound = df[column_name].quantile(lower_percentile / 100)
        upper_bound = df[column_name].quantile(upper_percentile / 100)
        
        filtered_df = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)].copy()
        
        # Log filtering results
        removed_count = len(df) - len(filtered_df)
        if removed_count > 0:
            print(f"Filtered {removed_count} outliers from '{column_name}' "
                  f"(bounds: {lower_bound:.2f} - {upper_bound:.2f})")
        
        return filtered_df
    
    def filter_by_time_interval(self, df: pd.DataFrame, interval: str) -> pd.DataFrame:
        """Filter DataFrame by time interval."""
        if df.empty or interval == 'All_Time':
            return df
        
        interval_config = self.config.time_intervals.get(interval)
        if not interval_config:
            return df
        
        days = interval_config.get('days')
        if not days or days == 'max':
            return df
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return df[df['Date'] >= cutoff_date].copy()
    
    def _calculate_price_change(self, df: pd.DataFrame, start_idx: int = -2, end_idx: int = -1) -> float:
        """Calculate percentage price change between two indices.
        
        Args:
            df: DataFrame with Close prices
            start_idx: Starting index (default -2 for 24h change)
            end_idx: Ending index (default -1 for latest)
        """
        if len(df) < abs(start_idx) + 1:
            return 0.0
        return (df['Close'].iloc[end_idx] - df['Close'].iloc[start_idx]) / df['Close'].iloc[start_idx] * 100
    
    def calculate_all_time_stats(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate all-time statistics across entire DataFrame.
        
        Returns:
            Dictionary with current_price, ath (all-time high), atl (all-time low), 
            avg_volume, price_change_24h
        """
        if df.empty:
            return {
                'current_price': 0,
                'ath': 0,
                'atl': 0,
                'avg_volume': 0,
                'price_change_24h': 0
            }
        
        return {
            'current_price': df['Close'].iloc[-1],
            'ath': df['High'].max(),
            'atl': df['Low'].min(),
            'avg_volume': df['Volume'].mean(),
            'price_change_24h': self._calculate_price_change(df, -2, -1)
        }
    
    def calculate_period_stats(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate statistics for a specific time period (filtered DataFrame).
        
        Returns:
            Dictionary with current_price, period_change, period_high, period_low, 
            avg_volume, data_points
        """
        if df.empty:
            return {
                'current_price': 0,
                'period_change': 0,
                'period_high': 0,
                'period_low': 0,
                'avg_volume': 0,
                'data_points': 0
            }
        
        return {
            'current_price': df['Close'].iloc[-1],
            'period_change': self._calculate_price_change(df, 0, -1),
            'period_high': df['High'].max(),
            'period_low': df['Low'].min(),
            'avg_volume': df['Volume'].mean(),
            'data_points': len(df)
        }
    
    def get_indicator_values(self, df: pd.DataFrame) -> Dict:
        """Extract technical indicator values from DataFrame (must have indicators added).
        
        Returns:
            Dictionary with sma_50, sma_200, ema_50, ema_200, and trend signal.
            Returns None for missing indicators.
        """
        if df.empty:
            return {
                'sma_50': None,
                'sma_200': None,
                'ema_50': None,
                'ema_200': None,
                'trend': None
            }
        
        # Get latest values if columns exist
        sma_50 = df['SMA_50'].iloc[-1] if 'SMA_50' in df.columns and not df['SMA_50'].isna().iloc[-1] else None
        sma_200 = df['SMA_200'].iloc[-1] if 'SMA_200' in df.columns and not df['SMA_200'].isna().iloc[-1] else None
        ema_50 = df['EMA_50'].iloc[-1] if 'EMA_50' in df.columns and not df['EMA_50'].isna().iloc[-1] else None
        ema_200 = df['EMA_200'].iloc[-1] if 'EMA_200' in df.columns and not df['EMA_200'].isna().iloc[-1] else None
        
        # Determine trend based on SMAs
        trend = None
        if sma_50 is not None and sma_200 is not None:
            trend = 'bullish' if sma_50 > sma_200 else 'bearish'
        
        return {
            'sma_50': sma_50,
            'sma_200': sma_200,
            'ema_50': ema_50,
            'ema_200': ema_200,
            'trend': trend
        }
    
    # Deprecated methods - kept for backward compatibility
    def get_symbol_stats(self, df: pd.DataFrame) -> Dict[str, float]:
        """Deprecated: Use calculate_all_time_stats() instead."""
        return self.calculate_all_time_stats(df)
    
    def calculate_basic_stats(self, df: pd.DataFrame) -> Dict[str, float]:
        """Deprecated: Use calculate_all_time_stats() or calculate_period_stats() instead."""
        stats = self.calculate_all_time_stats(df)
        return {
            'latest_price': stats['current_price'],
            'price_change_24h': stats['price_change_24h'],
            'high_price': stats['ath'],
            'low_price': stats['atl'],
            'data_points': len(df) if not df.empty else 0
        }
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> Dict:
        """Deprecated: Use add_technical_indicators() then get_indicator_values() instead."""
        return self.get_indicator_values(df)
    
    def fetch_multiple_symbols(self, symbols: List[str]) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple symbols."""
        result = {}
        for symbol in symbols:
            df = self.fetch_historical_data(symbol)
            if not df.empty:
                df = self.add_moving_averages(df)
                result[symbol] = df
        return result
    
    def calculate_rolling_correlation(self, df1: pd.DataFrame, df2: pd.DataFrame, window: int = 30) -> pd.Series:
        """Calculate rolling Pearson correlation between two price series.
        
        Args:
            df1: First DataFrame with 'Close' prices
            df2: Second DataFrame with 'Close' prices (typically BTC)
            window: Rolling window size in periods (default 30)
        
        Returns:
            Series with rolling correlation values (-1 to +1)
            Values > 0.7: Strong coupling
            Values 0.3-0.7: Moderate correlation
            Values < 0.3: Decoupling
        """
        if df1.empty or df2.empty:
            return pd.Series(dtype=float)
        
        # Align dataframes by date
        merged = pd.merge(df1[['Date', 'Close']], df2[['Date', 'Close']], 
                         on='Date', suffixes=('_1', '_2'))
        
        if len(merged) < window:
            return pd.Series(dtype=float)
        
        # Calculate rolling correlation
        correlation = merged['Close_1'].rolling(window=window).corr(merged['Close_2'])
        
        return correlation
    
    def calculate_beta_coefficient(self, df_asset: pd.DataFrame, df_market: pd.DataFrame, window: int = 30) -> pd.Series:
        """Calculate rolling beta coefficient (market sensitivity).
        
        Beta measures how much an asset moves relative to market (BTC) movements.
        
        Args:
            df_asset: Asset DataFrame with 'Close' prices
            df_market: Market DataFrame with 'Close' prices (typically BTC)
            window: Rolling window size in periods (default 30)
        
        Returns:
            Series with beta values:
            Beta > 1: Asset is more volatile than market (amplified movements)
            Beta = 1: Moves in line with market
            Beta < 1: Less volatile than market
            Beta < 0: Moves opposite to market
        """
        if df_asset.empty or df_market.empty:
            return pd.Series(dtype=float)
        
        # Align dataframes by date
        merged = pd.merge(df_asset[['Date', 'Close']], df_market[['Date', 'Close']], 
                         on='Date', suffixes=('_asset', '_market'))
        
        if len(merged) < window + 1:
            return pd.Series(dtype=float)
        
        # Calculate returns
        merged['return_asset'] = merged['Close_asset'].pct_change()
        merged['return_market'] = merged['Close_market'].pct_change()
        
        # Calculate rolling beta: Covariance(asset, market) / Variance(market)
        def rolling_beta(returns_asset, returns_market):
            covariance = returns_asset.cov(returns_market)
            variance = returns_market.var()
            if variance == 0 or pd.isna(variance):
                return float('nan')
            return covariance / variance
        
        beta = merged['return_asset'].rolling(window=window).apply(
            lambda x: rolling_beta(x, merged['return_market'].loc[x.index]), 
            raw=False
        )
        
        return beta
    
    def get_latest_correlation_beta(self, df_asset: pd.DataFrame, df_btc: pd.DataFrame, window: int = 30) -> Tuple[float, float]:
        """Get the latest correlation and beta values for an asset vs BTC.
        
        Args:
            df_asset: Asset DataFrame
            df_btc: Bitcoin DataFrame
            window: Rolling window size (default 30)
        
        Returns:
            Tuple of (correlation, beta) - both as floats
        """
        correlation_series = self.calculate_rolling_correlation(df_asset, df_btc, window)
        beta_series = self.calculate_beta_coefficient(df_asset, df_btc, window)
        
        correlation = correlation_series.iloc[-1] if not correlation_series.empty and not pd.isna(correlation_series.iloc[-1]) else 0.0
        beta = beta_series.iloc[-1] if not beta_series.empty and not pd.isna(beta_series.iloc[-1]) else 0.0
        
        return correlation, beta
