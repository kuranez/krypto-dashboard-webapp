# Data & Figures

## Data Manager (`web/app/data_manager.py`)
- Fetching: `fetch_combined_data(symbol)`
- Filtering: `filter_by_time_interval(df, period)`, `filter_price_spikes(df, spike_threshold)`
- Stats: `calculate_all_time_stats(df)`, `calculate_period_stats(df)`
- Indicators: `add_technical_indicators(df)`, `get_indicator_values(df)`

## Figure Factory (`web/app/figure_factory.py`)
- Colors: `convert_color(color_name, opacity=0.8)`
- Simple Line: `create_simple_price_chart(df, symbol, title=None)`
- Detailed: `create_detailed_price_figure(df, symbol, period, mapped_range=None, legend_config=None, margins=None)`
- Candlestick: `create_candlestick(df, title=None, x_range=None, margins=None)`
- Volume Only: `create_volume_only(df, title=None, x_range=None, margins=None)`

### Usage Examples

```python
from figure_factory import FigureFactory
from components.layouts import standard_margins

ff = FigureFactory()

# Assume df_period is a DataFrame with columns: Date, Open, High, Low, Close, Volume
# and x_range is a tuple like (start_date, end_date)

# Candlestick chart
fig_candle = ff.create_candlestick(
	df_period,
	title=f"{symbol} Candlestick Chart ({period})",
	x_range=x_range,
	margins=standard_margins(140, 180)
)

# Volume-only chart
fig_volume = ff.create_volume_only(
	df_period,
	title=f"{symbol} Trading Volume ({period})",
	x_range=x_range,
	margins=standard_margins(140, 180)
)

# Display with Panel
import panel as pn
pn.Row(pn.pane.Plotly(fig_candle), pn.pane.Plotly(fig_volume)).servable()
```
