from typing import Dict


def plotly_legend_config(title_text: str = "") -> Dict:
    return dict(
        orientation="h",
        yanchor="top",
        y=1.15,
        xanchor="center",
        x=0.5,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="rgba(71, 53, 106, 0.3)",
        borderwidth=1,
        font=dict(size=18),
        title=dict(
            text=title_text,
            font=dict(size=14, color="#47356A"),
            side="top"
        ),
        itemsizing="constant",
        tracegroupgap=15
    )


def standard_margins(top: int = 120, bottom: int = 160, left: int = 24, right: int = 24) -> Dict:
    return dict(l=left, r=right, t=top, b=bottom)
