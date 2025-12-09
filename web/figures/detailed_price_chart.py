"""
Detailed Price Chart
Creates comprehensive price charts with technical indicators and volume.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from components.colors import to_rgba
import pandas as pd
from typing import Optional, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from app.config import AppConfig


def _ensure_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add required technical indicators if missing."""
    df = df.copy()
    if 'SMA_50' not in df.columns:
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
    if 'SMA_200' not in df.columns:
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
    if 'EMA_50' not in df.columns:
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    if 'EMA_200' not in df.columns:
        df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    return df


def _get_resample_period(
    period: str, 
    date_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None
) -> str:
    """
    Determine the appropriate resampling period (Day, Week, Month) 
    based on the selected time period or date range.
    """
    if date_range:
        days = (date_range[1] - date_range[0]).days
        if days <= 90:  # Up to ~3 months
            return 'D'
        elif days <= 730:  # Up to 2 years
            return 'W'
        else:
            return 'M'

    if period in ['2Y', '3Y', '5Y', 'All_Time']:
        return 'M'  # Month
    elif period in ['3M', '6M', '1Y']:
        return 'W'  # Week
    else:
        return 'D'  # Day


def _aggregate_volume(
    df: pd.DataFrame, 
    period: str, 
    date_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None
) -> pd.DataFrame:
    """Aggregate volume by day/week/month depending on selected period."""
    resample_period = _get_resample_period(period, date_range)
    
    # Set 'Date' as the index for resampling
    df_resample = df.set_index('Date')
    
    # Resample the data
    df_agg = df_resample.resample(resample_period).agg({
        'Volume': 'sum',
        'Close': 'last',
        'Open': 'first'
    }).dropna().reset_index()
    
    return df_agg


def create_detailed_price_figure(
    df: pd.DataFrame,
    symbol: str,
    period: str,
    mapped_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
    legend_config: Optional[Dict] = None,
    margins: Optional[Dict] = None,
    config: Optional['AppConfig'] = None
) -> go.Figure:
    """
    Create the detailed price + indicators + volume figure used in the detailed dashboard.
    
    Args:
        df: DataFrame with OHLCV data
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        period: Time period string (e.g., '1Y', '3M')
        mapped_range: Optional tuple of (start_date, end_date) for x-axis range
        legend_config: Optional dict for legend configuration
        margins: Optional dict of margins (l, r, t, b)
        config: Optional AppConfig instance (creates new if not provided)
    
    Returns:
        Plotly Figure object with subplots for price+indicators and volume
    """
    if config is None:
        from app.config import AppConfig
        config = AppConfig()

    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available", 
            xref="paper", yref="paper", 
            x=0.5, y=0.5, showarrow=False, 
            font=dict(size=16)
        )
        return fig

    df = _ensure_indicators(df)

    primary_color = config.get_crypto_color(symbol, 'primary')
    secondary_color = config.get_crypto_color(symbol, 'secondary')

    # ...removed local to_rgba...

    color_a = to_rgba(primary_color, 0.8)
    color_b = to_rgba(secondary_color, 0.6)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.8, 0.2],
        subplot_titles=(f'{symbol} Price Chart ({period})', 'Trading Volume')
    )

    # Style subplot titles (if any annotations exist)
    annotations = getattr(fig.layout, 'annotations', None)
    if annotations:
        for annotation in annotations:
            annotation.update(font=dict(size=18, color='#47356A'), y=annotation.y + 0.03)

    # Price traces
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['High'], mode='lines', name='High',
        line=dict(color=to_rgba(primary_color, 0.4), width=1),
        hovertemplate='<b>High</b>: <b>$%{y:,.2f}</b><extra></extra>'
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Low'], mode='lines', name='Low',
        line=dict(color=to_rgba(secondary_color, 0.4), width=1),
        hovertemplate='<b>Low</b>: <b>$%{y:,.2f}</b><extra></extra>'
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Close'], mode='lines', name='Close',
        line=dict(color=color_a, width=2),
        hovertemplate='<b>Close</b>: <b>$%{y:,.2f}</b><extra></extra>'
    ), row=1, col=1)

    # SMA/EMA indicators
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['SMA_50'], mode='lines', name='SMA 50',
        line=dict(color='rgba(231, 76, 60, 0.8)', width=1.5, dash='dash'),
        hovertemplate='<b>SMA 50</b>: <b>$%{y:,.2f}</b><extra></extra>'
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['SMA_200'], mode='lines', name='SMA 200',
        line=dict(color='rgba(155, 89, 182, 0.8)', width=1.5, dash='dash'),
        hovertemplate='<b>SMA 200</b>: <b>$%{y:,.2f}</b><extra></extra>'
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['EMA_50'], mode='lines', name='EMA 50',
        line=dict(color='rgba(243, 156, 18, 0.8)', width=1.5, dash='dot'),
        hovertemplate='<b>EMA 50</b>: <b>$%{y:,.2f}</b><extra></extra>'
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['EMA_200'], mode='lines', name='EMA 200',
        line=dict(color='rgba(26, 188, 156, 0.8)', width=1.5, dash='dot'),
        hovertemplate='<b>EMA 200</b>: <b>$%{y:,.2f}</b><extra></extra>'
    ), row=1, col=1)

    # Volume subplot
    df_volume = _aggregate_volume(df, period, mapped_range)
    colors = [
        'rgba(26, 188, 156, 0.8)' if close >= open_ else 'rgba(231, 76, 60, 0.8)'
        for close, open_ in zip(df_volume['Close'], df_volume['Open'])
    ]
    
    fig.add_trace(go.Bar(
        x=df_volume['Date'], y=df_volume['Volume'], name='Volume',
        marker_color=colors,
        hovertemplate='Volume: <b>%{y:,.0f}</b><extra></extra>'
    ), row=2, col=1)

    # Layout configuration
    fig.update_layout(
        template=config.get_plotly_template(),
        hovermode='x unified',
        hoverlabel=dict(font_size=14),
        showlegend=True,
        legend=legend_config or {},
        xaxis2_title="Date",
        yaxis_title="Price (USD)",
        yaxis2_title="Volume",
        xaxis_rangeslider_visible=False,
        autosize=True,
        margin=margins or dict(l=50, r=50, t=50, b=50)
    )

    if mapped_range:
        fig.update_xaxes(range=mapped_range)
        
        # Autoscale volume y-axis based on the visible date range
        try:
            start_date, end_date = pd.to_datetime(mapped_range[0]), pd.to_datetime(mapped_range[1])
            visible_volume_df = df_volume[
                (df_volume['Date'] >= start_date) & (df_volume['Date'] <= end_date)
            ]
            if not visible_volume_df.empty:
                max_volume = visible_volume_df['Volume'].max()
                fig.update_yaxes(row=2, col=1, range=[0, max_volume * 1.15])  # Add 15% padding
        except Exception:
            # Fallback to default autoscaling if range parsing fails
            pass

    # Grid styling
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
    fig.update_yaxes(row=2, col=1, tickformat='.2s')

    return fig
