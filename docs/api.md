# API / Method Index

Complete list of primary classes and methods across the project.

## App Layer (`web/app`)

### `base_dashboard.py`
- Class `BaseDashboard`
  - `_create_footer_row()`
  - `create_dashboard()` (to be overridden)
  - `refresh_data()` (to be overridden)
  - `get_dependencies()`

### `main.py`
- Exposes Panel app `app`
- Registers dashboards and routes

### `launch.py`
- `main()` — dev runner with port fallback and path setup

### `figure_factory.py`
- Class `FigureFactory`
  - `convert_color(color_name, opacity=0.8)`
  - `create_simple_price_chart(df, symbol, title=None)`
  - `create_detailed_price_figure(df, symbol, period, mapped_range=None, legend_config=None, margins=None)`
  - `create_candlestick(df, title=None, x_range=None, margins=None)`
  - `create_volume_only(df, title=None, x_range=None, margins=None)`

### `data_manager.py`
- Class `DataManager`
  - `fetch_combined_data(symbol)`
  - `filter_by_time_interval(df, period)`
  - `filter_price_spikes(df, spike_threshold)`
  - `calculate_all_time_stats(df)`
  - `calculate_period_stats(df)`
  - `add_technical_indicators(df)`
  - `get_indicator_values(df)`

### `config.py`
- Class `AppConfig`
  - `get_plotly_template()`
  - `get_crypto_color(symbol, variant)`
  - `time_intervals` (mapping)
  - `styles` (dict)

## Dashboards (`web/dashboards`)

### `simple_price_dashboard.py`
- Class `SimplePriceDashboard`
  - `_create_widgets()`
  - `_on_symbol_change(event)`
  - `_on_period_change(event)`
  - `_on_range_idx_change(event)`
  - `_on_chart_type_change(event)`
  - `_on_refresh_click(event)`
  - `_load_initial_data()`
  - `_load_data()`
  - `_create_price_chart()`
  - `_create_info_panel()`
  - `create_dashboard()`
  - `_update_display()`
  - `refresh_data()`
  - `get_dependencies()`

### `detailed_price_chart.py`
- Class `DetailedPriceDashboard`
  - `_create_widgets()`
  - `_on_symbol_change(event)`
  - `_on_period_change(event)`
  - `_on_range_idx_change(event)`
  - `_load_data()`
  - `_create_price_chart()`
  - `_create_info_panel()`
  - `create_dashboard()`
  - `_update_display()`
  - `refresh_data()`
  - `get_dependencies()`

### `market_overview.py`
- Class `MarketOverviewDashboard`
  - Methods aligned to build overview charts, controls, and info panes

## Components (`web/components`)

### `widgets.py`
- `create_symbol_selector(options, default)`
- `create_period_selector(options, default)`
- `create_range_widgets()`

### `ui.py`
- `create_header(title, color)`
- `create_summary_box(text, border_color)`

### `explanations.py`
- `technical_analysis_guide()`
- `market_coupling_explanation()`

### `layouts.py`
- `plotly_legend_config(title_text)`
- `standard_margins(top, bottom, left=50, right=50)`

## Testing (`testing`)
- `test_correlation.py` — correlation tests
- `conftest.py` — shared fixtures

---

Note: This index focuses on project-level public methods. Internal helpers may be omitted. For an auto-generated index, consider `pdoc` or `sphinx` with docstrings.
