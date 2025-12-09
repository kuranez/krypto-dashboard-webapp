"""
Candlestick Chart
Creates candlestick charts for OHLC data visualization.
"""

import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from app.config import AppConfig


def create_candlestick(
    df: pd.DataFrame,
    title: Optional[str] = None,
    x_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
    margins: Optional[Dict] = None,
    config: Optional['AppConfig'] = None
) -> go.Figure:
    """
    Create a candlestick figure with standardized layout.
    
    Args:
        df: DataFrame with 'Date', 'Open', 'High', 'Low', 'Close' columns
        title: Optional chart title
        x_range: Optional tuple of (start_date, end_date) for x-axis range
        margins: Optional dict of margins (l, r, t, b)
        config: Optional AppConfig instance (creates new if not provided)
    
    Returns:
        Plotly Figure object
    """
    if config is None:
        from app.config import AppConfig
        config = AppConfig()
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])
    
    fig.update_layout(
        title=title or "Candlestick",
        title_font_size=18,
        hoverlabel=dict(font_size=14),
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template=config.get_plotly_template(),
        xaxis_rangeslider_visible=True,
        autosize=True,
        margin=margins or dict(l=50, r=50, t=50, b=50)
    )
    
    if x_range:
        fig.update_xaxes(range=x_range)
    
    return fig
