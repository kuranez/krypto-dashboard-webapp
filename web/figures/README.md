# Figures Module

This module contains specialized figure creation functions for different chart types used in the cryptocurrency dashboard.

## Structure

The figures module is organized into separate files by chart type for better code organization and maintainability:

- **`simple_price_chart.py`** - Basic price charts with fill for single cryptocurrencies
- **`candlestick_chart.py`** - OHLC candlestick charts
- **`volume_chart.py`** - Trading volume bar charts
- **`detailed_price_chart.py`** - Comprehensive charts with technical indicators (SMA/EMA) and volume subplots

## Usage

### Direct Import

```python
from figures import (
    create_simple_price_chart,
    create_candlestick,
    create_volume_only,
    create_detailed_price_figure
)

# Create a simple price chart
fig = create_simple_price_chart(df, symbol='BTC', title='BTC Price')
```

### Via FigureFactory

The recommended way to use these functions is through the `FigureFactory` class in `app/figure_factory.py`:

```python
from app.figure_factory import FigureFactory

factory = FigureFactory()
fig = factory.create_simple_price_chart(df, 'BTC', 'BTC Price Chart')
```

## Design Principles

1. **Modularity**: Each chart type is in its own file for easier maintenance
2. **Separation of Concerns**: Chart creation logic is separate from dashboard logic
3. **Dependency Injection**: `AppConfig` is passed as a parameter to avoid circular imports
4. **Type Safety**: Uses TYPE_CHECKING to provide type hints without runtime imports

## Function Signatures

### create_simple_price_chart
Creates a basic line chart with fill area.
- **Parameters**: df, symbol, title (optional), config (optional)
- **Returns**: Plotly Figure

### create_candlestick
Creates a candlestick chart for OHLC data.
- **Parameters**: df, title (optional), x_range (optional), margins (optional), config (optional)
- **Returns**: Plotly Figure

### create_volume_only
Creates a volume bar chart.
- **Parameters**: df, title (optional), x_range (optional), margins (optional), config (optional)
- **Returns**: Plotly Figure

### create_detailed_price_figure
Creates a comprehensive chart with price, indicators, and volume subplots.
- **Parameters**: df, symbol, period, mapped_range (optional), legend_config (optional), margins (optional), config (optional)
- **Returns**: Plotly Figure with subplots

## Dependencies

- `plotly` - Chart rendering
- `pandas` - Data handling
- `matplotlib` - Color utilities
- `app.config.AppConfig` - Configuration (injected at runtime)
