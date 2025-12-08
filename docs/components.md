# Shared Components

## Widgets (`components/widgets.py`)
- `create_symbol_selector(options, default)`
- `create_period_selector(options, default)`
- `create_range_widgets()` → returns `(range_idx, range_label)` with hidden slider values and styled label

## UI (`components/ui.py`)
- `create_header(title, color)`
- `create_summary_box(text, border_color)`

## Explanations (`components/explanations.py`)
- `technical_analysis_guide()`
- `market_coupling_explanation()`

## Layouts (`components/layouts.py`)
- `plotly_legend_config(title_text)`
- `standard_margins(top, bottom, left=50, right=50)`
