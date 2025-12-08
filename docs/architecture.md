# Architecture Overview

## High-Level
- UI Framework: Panel (Rows/Columns, panes, widgets)
- Charts: Plotly (Graph Objects, subplots)
- Data: Pandas dataframes via `DataManager`
- Config: `AppConfig` for styles, time intervals, colors
- Modular Dashboards: `web/dashboards/*`
- Shared Components: `web/components/*`
- App Entrypoint: `web/app/main.py` and `web/app/launch.py`

## Folder Structure
```
web/
  app/
    main.py            # Mount dashboards and template
    launch.py          # Local dev runner (app.show)
    base_dashboard.py  # Common behaviors & footer
    figure_factory.py  # Centralized Plotly figure creation
    config.py          # App-wide configuration
    data_manager.py    # Data fetching, filtering, stats, indicators
  dashboards/
    simple_price_dashboard.py
    detailed_price_chart.py
    market_overview.py
  components/
    widgets.py         # Selectors, range slider + label
    ui.py              # Header, summary box
    explanations.py    # Reusable markdown panes
    layouts.py         # Legend config + margins helpers
```

## Runtime Flow
1. User opens app via `launch.py` (Panel) or `panel serve main.py`.
2. `main.py` registers dashboards and builds the UI template.
3. Each dashboard:
   - Creates widgets via `components/widgets.py`.
   - Fetches/filters data via `DataManager`.
   - Builds charts via `FigureFactory`.
   - Renders layout (header, summary, controls, chart, info, footer).

## Key Design Decisions
- Shared components for consistency and maintainability.
- Index-based date slider for deterministic range control.
- FigureFactory centralizes Plotly construction and styling.
- Layout helpers to standardize margins and legend presentation.
