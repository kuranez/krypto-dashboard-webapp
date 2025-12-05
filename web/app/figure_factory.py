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
            hovertemplate=f'{symbol}<br>Date: %{{x}}<br>Price: $ %{{y:,.2f}}<extra></extra>'
        ))
        
        # Calculate price range for better y-axis
        price_min = df['Close'].min()
        price_max = df['Close'].max()
        price_range = price_max - price_min
        
        fig.update_layout(
            title_text=title or f"{symbol} Price Chart",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template=self.config.get_plotly_template(),
            showlegend=False,
            yaxis=dict(
                range=[price_min - price_range * 0.1, price_max + price_range * 0.1]
            ),
            xaxis=dict(
                rangeslider=dict(visible=True, thickness=0.05),
                type='date'
            ),
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
