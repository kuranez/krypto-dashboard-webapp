"""
Volume Chart
Creates volume bar charts for trading volume visualization.
"""

import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from app.config import AppConfig


def create_volume_only(
    df: pd.DataFrame,
    title: Optional[str] = None,
    x_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
    margins: Optional[Dict] = None,
    config: Optional['AppConfig'] = None
) -> go.Figure:
    """
    Create a volume bar chart with standardized layout.
    
    Args:
        df: DataFrame with 'Date' and 'Volume' columns
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
    
    # Use red/green colors for volume bars based on price movement if 'Open' and 'Close' columns are present.
    if 'Open' in df.columns and 'Close' in df.columns:
        bar_colors = [
            config.green_color if close >= open_ else config.red_color
            for open_, close in zip(df['Open'], df['Close'])
        ]
    else:
        # Default to blue if price columns are missing
        bar_colors = [config.blue_color] * len(df)

    fig = go.Figure(data=[go.Bar(
        x=df['Date'],
        y=df['Volume'],
        marker_color=bar_colors
    )])

    fig.update_layout(
        title=title or "Trading Volume",
        title_font_size=18,
        hoverlabel=dict(font_size=14),
        xaxis_title="Date",
        yaxis_title="Volume",
        template=config.get_plotly_template(),
        autosize=True,
        margin=margins or dict(l=50, r=50, t=50, b=50)
    )

    if x_range:
        fig.update_xaxes(range=x_range)

    return fig
