"""
Figure Factory
Centralized figure creation and styling utilities.
"""

import plotly.graph_objects as go
import matplotlib.colors as mcolors
import pandas as pd
from typing import Dict, List, Optional, Tuple
from config import AppConfig

class FigureFactory:
    """Factory class for creating standardized Plotly figures."""
    
    def __init__(self):
        self.config = AppConfig()
    
    def convert_color(self, color_name: str, opacity: float = 0.8) -> str:
        """Convert a color name to rgba format."""
        rgba = mcolors.to_rgba(color_name, opacity)
        return f'rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {rgba[3]})'
    
    def create_simple_price_chart(self, 
                                  df: pd.DataFrame, 
                                  symbol: str,
                                  title: Optional[str] = None) -> go.Figure:
        """Create a simple price chart for a single symbol."""
        
        if df.empty:
            # Return empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        fig = go.Figure()
        
        primary_color = self.config.get_crypto_color(symbol, 'primary')
        secondary_color = self.config.get_crypto_color(symbol, 'secondary')
        
        # Add price line with fill
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Close'],
            mode='lines',
            name=f'{symbol} Price',
            line=dict(color=self.convert_color(primary_color, 0.8), width=2),
            fill='tozeroy',
            fillcolor=self.convert_color(secondary_color, 0.3),
            hovertemplate=f'<b>{symbol}</b><br>Date: <b>%{{x}}</b><br>Price: <b>$ %{{y:,.2f}}</b><extra></extra>'
        ))
        
        # Calculate price range for better y-axis
        price_min = df['Close'].min()
        price_max = df['Close'].max()
        price_range = price_max - price_min
        
        fig.update_layout(
            title_text=title or f"{symbol} Price Chart",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template=self.config.get_plotly_template(),
            showlegend=False,
            yaxis=dict(
                range=[price_min - price_range * 0.1, price_max + price_range * 0.1]
            ),
            xaxis=dict(
                rangeslider=dict(visible=False, thickness=0.05),
                type='date'
            ),
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig

    def create_candlestick(self,
                            df: pd.DataFrame,
                            title: Optional[str] = None,
                            x_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
                            margins: Optional[Dict] = None) -> go.Figure:
        """Create a candlestick figure with standardized layout."""
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
            template=self.config.get_plotly_template(),
            xaxis_rangeslider_visible=True,
            autosize=True,
            margin=margins or dict(l=50, r=50, t=50, b=50)
        )
        if x_range:
            fig.update_xaxes(range=x_range)
        return fig

    def create_volume_only(self,
                            df: pd.DataFrame,
                            title: Optional[str] = None,
                            x_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
                            margins: Optional[Dict] = None) -> go.Figure:
        """Create a volume bar chart with standardized layout."""
        fig = go.Figure(data=[go.Bar(
            x=df['Date'],
            y=df['Volume'],
            marker_color='#3498db'
        )])
        fig.update_layout(
            title=title or "Trading Volume",
            title_font_size=18,
            hoverlabel=dict(font_size=14),
            xaxis_title="Date",
            yaxis_title="Volume",
            template=self.config.get_plotly_template(),
            autosize=True,
            margin=margins or dict(l=50, r=50, t=50, b=50)
        )
        if x_range:
            fig.update_xaxes(range=x_range)
        return fig

    def _ensure_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
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

    def _aggregate_volume(self, df: pd.DataFrame, period: str) -> pd.DataFrame:
        """Aggregate volume by day/week/month depending on selected period."""
        if period in ['2Y', '3Y', '5Y', 'All_Time']:
            df_copy = df.copy()
            df_copy['Month'] = df_copy['Date'].dt.to_period('M').apply(lambda r: r.start_time)
            df_volume = df_copy.groupby('Month').agg({'Volume': 'sum', 'Close': 'last', 'Open': 'first'}).reset_index()
            df_volume.rename(columns={'Month': 'Date'}, inplace=True)
        elif period in ['3M', '6M', '1Y']:
            df_copy = df.copy()
            df_copy['Week'] = df_copy['Date'].dt.to_period('W').apply(lambda r: r.start_time)
            df_volume = df_copy.groupby('Week').agg({'Volume': 'sum', 'Close': 'last', 'Open': 'first'}).reset_index()
            df_volume.rename(columns={'Week': 'Date'}, inplace=True)
        else:
            df_volume = df.groupby('Date').agg({'Volume': 'sum', 'Close': 'last', 'Open': 'first'}).reset_index()
        return df_volume

    def create_detailed_price_figure(
        self,
        df: pd.DataFrame,
        symbol: str,
        period: str,
        mapped_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
        legend_config: Optional[Dict] = None,
        margins: Optional[Dict] = None
    ) -> go.Figure:
        """Create the detailed price + indicators + volume figure used in the detailed dashboard."""
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import matplotlib.colors as mcolors

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=16))
            return fig

        df = self._ensure_indicators(df)

        primary_color = self.config.get_crypto_color(symbol, 'primary')
        secondary_color = self.config.get_crypto_color(symbol, 'secondary')

        def to_rgba(color_name, opacity=1.0):
            rgba = mcolors.to_rgba(color_name, opacity)
            return f'rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {rgba[3]})'

        color_a = to_rgba(primary_color, 0.8)
        color_b = to_rgba(secondary_color, 0.6)

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=[0.8, 0.2],
            subplot_titles=(f'{symbol} Price Chart ({period})', 'Trading Volume')
        )

        for annotation in fig.layout.annotations:
            annotation.update(font=dict(size=18, color='#47356A'), y=annotation.y + 0.03)

        # Price traces
        fig.add_trace(go.Scatter(x=df['Date'], y=df['High'], mode='lines', name='High',
                                 line=dict(color=to_rgba(primary_color, 0.4), width=1),
                                 hovertemplate='<b>High</b>: <b>$%{y:,.2f}</b><extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Low'], mode='lines', name='Low',
                                 line=dict(color=to_rgba(secondary_color, 0.4), width=1),
                                 hovertemplate='<b>Low</b>: <b>$%{y:,.2f}</b><extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close',
                                 line=dict(color=color_a, width=2),
                                 hovertemplate='<b>Close</b>: <b>$%{y:,.2f}</b><extra></extra>'), row=1, col=1)

        # SMA/EMA
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', name='SMA 50',
                                 line=dict(color='rgba(231, 76, 60, 0.8)', width=1.5, dash='dash'),
                                 hovertemplate='<b>SMA 50</b>: <b>$%{y:,.2f}</b><extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', name='SMA 200',
                                 line=dict(color='rgba(155, 89, 182, 0.8)', width=1.5, dash='dash'),
                                 hovertemplate='<b>SMA 200</b>: <b>$%{y:,.2f}</b><extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_50'], mode='lines', name='EMA 50',
                                 line=dict(color='rgba(243, 156, 18, 0.8)', width=1.5, dash='dot'),
                                 hovertemplate='<b>EMA 50</b>: <b>$%{y:,.2f}</b><extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_200'], mode='lines', name='EMA 200',
                                 line=dict(color='rgba(26, 188, 156, 0.8)', width=1.5, dash='dot'),
                                 hovertemplate='<b>EMA 200</b>: <b>$%{y:,.2f}</b><extra></extra>'), row=1, col=1)

        # Volume
        df_volume = self._aggregate_volume(df, period)
        colors = ['rgba(26, 188, 156, 0.8)' if close >= open_ else 'rgba(231, 76, 60, 0.8)'
                  for close, open_ in zip(df_volume['Close'], df_volume['Open'])]
        fig.add_trace(go.Bar(x=df_volume['Date'], y=df_volume['Volume'], name='Volume',
                             marker_color=colors,
                             hovertemplate='Volume: <b>%{y:,.0f}</b><extra></extra>'), row=2, col=1)

        # Layout
        fig.update_layout(
            template=self.config.get_plotly_template(),
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

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        fig.update_yaxes(row=2, col=1, tickformat='.2s')

        return fig
