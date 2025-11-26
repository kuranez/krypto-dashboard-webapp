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
                             interval: str = '1d', 
                             start_time: Optional[int] = None, 
                             end_time: Optional[int] = None, 
                             limit: int = 1000) -> pd.DataFrame:
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
    
    def add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add Simple and Exponential Moving Averages to the DataFrame."""
        if df.empty:
            return df
            
        df = df.copy()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
        
        return df
    
    def filter_by_time_interval(self, df: pd.DataFrame, interval: str) -> pd.DataFrame:
        """Filter DataFrame by time interval."""
        if df.empty or interval == 'All_Time':
            return df
        
        days = self.config.time_intervals.get(interval)
        if not days:
            return df
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return df[df['Date'] >= cutoff_date].copy()
    
    def get_symbol_stats(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate basic statistics for a symbol."""
        if df.empty:
            return {}
        
        return {
            'current_price': df['Close'].iloc[-1] if len(df) > 0 else 0,
            'ath': df['High'].max(),
            'atl': df['Low'].min(),
            'avg_volume': df['Volume'].mean(),
            'price_change_24h': (df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2] * 100 if len(df) > 1 else 0
        }
    
    def fetch_multiple_symbols(self, symbols: List[str]) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple symbols."""
        result = {}
        for symbol in symbols:
            df = self.fetch_historical_data(symbol)
            if not df.empty:
                df = self.add_moving_averages(df)
                result[symbol] = df
        return result
