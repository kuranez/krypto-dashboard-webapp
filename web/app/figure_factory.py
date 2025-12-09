"""
Figure Factory
Centralized figure creation and styling utilities.
This factory delegates to specialized figure modules for better code organization.
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Optional, Tuple

from components.colors import to_rgba
from config import AppConfig
from figures import (
    create_simple_price_chart as _create_simple_price_chart,
    create_candlestick as _create_candlestick,
    create_volume_only as _create_volume_only,
    create_detailed_price_figure as _create_detailed_price_figure,
)


class FigureFactory:
    """Factory class for creating standardized Plotly figures."""
    
    def __init__(self):
        self.config = AppConfig()
    
    def convert_color(self, color_name: str, opacity: float = 0.8) -> str:
        """Convert a color name to rgba format using shared utility."""
        return to_rgba(color_name, opacity)
    
    def create_simple_price_chart(self, 
                                  df: pd.DataFrame, 
                                  symbol: str,
                                  title: Optional[str] = None) -> go.Figure:
        """Create a simple price chart for a single symbol."""
        return _create_simple_price_chart(df, symbol, title, self.config)

    def create_candlestick(self,
                            df: pd.DataFrame,
                            title: Optional[str] = None,
                            x_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
                            margins: Optional[Dict] = None) -> go.Figure:
        """Create a candlestick figure with standardized layout."""
        return _create_candlestick(df, title, x_range, margins, self.config)

    def create_volume_only(self,
                            df: pd.DataFrame,
                            title: Optional[str] = None,
                            x_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
                            margins: Optional[Dict] = None) -> go.Figure:
        """Create a volume bar chart with standardized layout."""
        return _create_volume_only(df, title, x_range, margins, self.config)

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
        return _create_detailed_price_figure(
            df, symbol, period, mapped_range, legend_config, margins, self.config
        )
