# Dashboard Development Guide

## Creating a Dashboard
- Inherit from `BaseDashboard`.
- Define `display_name`, `description`, `version`, `author`.
- Initialize `AppConfig`, `DataManager`, `FigureFactory`.
- Create widgets using `components/widgets.py`:
  - `create_symbol_selector(options, default)`
  - `create_period_selector(options, default)`
  - `create_range_widgets()` → returns `(range_idx, range_label)`
- Bind events: symbol/period changes, range slider updates.
- Implement `_load_data()` using `DataManager.fetch_combined_data()` and optional `filter_price_spikes()`.
- Implement `_create_price_chart()` using `FigureFactory`.
- Implement `_create_info_panel()` for stats using `DataManager`.
- Build layout in `create_dashboard()`:
  - Header via `components/ui.create_header()`
  - Summary via `components/ui.create_summary_box()`
  - Controls: Row 1 (selectors + range_label), Row 2 (range_idx)
  - Main Row: chart pane + info pane
  - Optional explanation pane from `components/explanations.py`
  - Footer via `BaseDashboard._create_footer_row()`

## Range Control Pattern
- Index-based `IntRangeSlider` for precision: 1 step ≈ 1 day.
- Map indices to dates and store `_mapped_date_range`.
- Update label to `#### Selected: YYYY-MM-DD → YYYY-MM-DD` with 20px font, color `#47356A`.
- Listen to Plotly `relayout_data` to sync zoom/pan back to `_mapped_date_range` + label.

## Figure Creation
- Use `FigureFactory.create_simple_price_chart()` for line charts.
- Use `FigureFactory.create_detailed_price_figure()` for detailed price + indicators + volume.
- Optional: `create_candlestick()` and `create_volume_only()` for simple dashboard parity.

## Styling & Layout
- Standardize margins via `components/layouts.standard_margins(top, bottom)`.
- Standardize legend via `components/layouts.plotly_legend_config(title_text)`.
- Use `self.config.get_plotly_template()` for template.
