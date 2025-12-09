from config import AppConfig
from typing import Dict

def plotly_legend_config(title_text: str = "") -> Dict:
    config = AppConfig()
    return dict(
        orientation="h",
        yanchor="top",
        y=1.15,
        xanchor="center",
        x=0.5,
        bgcolor=config.white_color,
        bordercolor=config.primary_color + '4D',  # 0.3 alpha as hex (4D)
        borderwidth=1,
        font=dict(size=18),
        title=dict(
            text=title_text,
            font=dict(size=14, color=config.primary_text_color),
            side="top"
        ),
        itemsizing="constant",
        tracegroupgap=15
    )


def standard_margins(top: int = 120, bottom: int = 160, left: int = 24, right: int = 24) -> Dict:
    return dict(l=left, r=right, t=top, b=bottom)
