import panel as pn
from config import AppConfig

def create_header(title: str, color: str) -> pn.pane.Markdown:
    return pn.pane.Markdown(
        f"## {title}",
        styles={
            'font-size': '24px',
            'color': color,
            'text-align': 'center'
        }
    )


def create_summary_box(text: str, border_color: str, config: AppConfig) -> pn.pane.Markdown:
    return pn.pane.Markdown(
        text,
        styles={
            'font-size': '16px',
            'background-color': config.light_gray_color,
            'color': config.secondary_text_color,
            'padding': '12px',
            'border-radius': '5px',
            'border-left': f'4px solid {border_color}',
            'margin': '6px 0'
        },
        sizing_mode='stretch_width'
    )
