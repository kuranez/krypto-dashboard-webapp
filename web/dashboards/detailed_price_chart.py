"""
Detailed Price Chart Dashboard
A detailed dashboard showing price chart with technical indicators and volume.
"""

import panel as pn
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from base_dashboard import BaseDashboard
from config import AppConfig
from data_manager import DataManager
from figure_factory import FigureFactory

from components.explanations import technical_analysis_guide
from components.layouts import plotly_legend_config, standard_margins
from components.ui import create_header, create_summary_box
from components.widgets import create_symbol_selector, create_period_selector, create_range_widgets


class DetailedPriceDashboard(BaseDashboard):
    """Detailed dashboard with price chart, technical indicators, and volume."""
    
    display_name = "Detailed Price Chart"
    description = "Detailed price chart with SMA/EMA indicators and volume"
    version = "2.6"
    author = "kuranez"
    
    def __init__(self):
        super().__init__()
        self.config = AppConfig()
        self.data_manager = DataManager()
        self.figure_factory = FigureFactory()
        
        # Dashboard state
        self.current_symbol = 'BTC'
        self.current_period = '1Y'
        
        # Available options
        self.available_symbols = self.config.available_symbols
        self.available_periods = list(self.config.time_intervals.keys())
        
        # Data storage
        self.current_data = None
        
        # Create widgets
        self._create_widgets()
        
    def _create_widgets(self):
        self.widgets['symbol_selector'] = create_symbol_selector(self.available_symbols, self.current_symbol)
        self.widgets['period_selector'] = create_period_selector(self.available_periods, self.current_period)
        self.widgets['range_idx'], self.widgets['range_label'] = create_range_widgets()
        # Bind
        self.widgets['symbol_selector'].param.watch(self._on_symbol_change, 'value')
        self.widgets['period_selector'].param.watch(self._on_period_change, 'value')
        self.widgets['range_idx'].param.watch(self._on_range_idx_change, 'value')

    def _on_symbol_change(self, event):
        self.current_symbol = event.new
        self._load_data()
        if hasattr(self, 'chart_pane'):
            self._update_display()

    def _on_period_change(self, event):
        self.current_period = event.new
        if self.current_data is not None and not self.current_data.empty:
            try:
                period_df = self.data_manager.filter_by_time_interval(self.current_data, self.current_period)
                if not period_df.empty:
                    n = len(period_df)
                    self.widgets['range_idx'].start = 0
                    self.widgets['range_idx'].end = max(1, n - 1)
                    self.widgets['range_idx'].value = (0, max(1, n - 1))
                    self.widgets['range_idx'].disabled = False
                    self._mapped_date_range = (period_df.iloc[0]['Date'], period_df.iloc[n - 1]['Date'])
                    self.widgets['range_label'].object = f"#### Selected: {period_df.iloc[0]['Date']:%Y-%m-%d} → {period_df.iloc[n-1]['Date']:%Y-%m-%d}"
            except Exception:
                pass
        if hasattr(self, 'chart_pane'):
            self._update_display()

    def _on_range_idx_change(self, event):
        try:
            df_period = self.data_manager.filter_by_time_interval(self.current_data, self.current_period)
            if df_period is not None and not df_period.empty:
                i_start, i_end = event.new
                i_start = max(0, min(i_start, len(df_period) - 1))
                i_end = max(0, min(i_end, len(df_period) - 1))
                if i_start > i_end:
                    i_start, i_end = i_end, i_start
                start_date = df_period.iloc[i_start]['Date']
                end_date = df_period.iloc[i_end]['Date']
                self.widgets['range_label'].object = f"#### Selected: {start_date:%Y-%m-%d} → {end_date:%Y-%m-%d}"
                self._mapped_date_range = (start_date, end_date)
                
                effective_period = self._get_effective_period(start_date, end_date)
                if self.current_period != effective_period:
                    self.widgets['period_selector'].value = effective_period

        except Exception:
            pass
        if hasattr(self, 'chart_pane'):
            self._update_display()

    def _get_effective_period(self, start_date, end_date):
        """Determine the most appropriate aggregation period based on the date range."""
        days = (end_date - start_date).days
        if days <= 31:
            return '1M'
        elif days <= 93:
            return '3M'
        elif days <= 186:
            return '6M'
        elif days <= 366:
            return '1Y'
        elif days <= 365 * 2:
            return '2Y'
        elif days <= 365 * 3:
            return '3Y'
        elif days <= 365 * 5:
            return '5Y'
        else:
            return 'All_Time'

    def _load_data(self):
        symbol_usdt = f"{self.current_symbol}USDT"
        try:
            df = self.data_manager.fetch_combined_data(symbol=symbol_usdt)
            if not df.empty:
                df = self.data_manager.filter_price_spikes(df, spike_threshold=4.0)
                self.current_data = df
            else:
                self.current_data = None
        except Exception as e:
            print(f"Error loading data: {e}")
            self.current_data = None
        if self.current_data is not None and not self.current_data.empty:
            try:
                period_df = self.data_manager.filter_by_time_interval(self.current_data, self.current_period)
                if not period_df.empty:
                    n = len(period_df)
                    self.widgets['range_idx'].start = 0
                    self.widgets['range_idx'].end = max(1, n - 1)
                    self.widgets['range_idx'].value = (0, max(1, n - 1))
                    self.widgets['range_idx'].disabled = False
                    self._mapped_date_range = (period_df.iloc[0]['Date'], period_df.iloc[n - 1]['Date'])
                    self.widgets['range_label'].object = f"#### Selected: {period_df.iloc[0]['Date']:%Y-%m-%d} → {period_df.iloc[n-1]['Date']:%Y-%m-%d}"
                else:
                    self.widgets['range_idx'].start = 0
                    self.widgets['range_idx'].end = 1
                    self.widgets['range_idx'].value = (0, 1)
                    self.widgets['range_idx'].disabled = True
            except Exception:
                self.widgets['range_idx'].start = 0
                self.widgets['range_idx'].end = 1
                self.widgets['range_idx'].value = (0, 1)
                self.widgets['range_idx'].disabled = True

    def _create_price_chart(self):
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("## No data available\n\nClick **Load Data** to load market data.")
        filtered_data = self.data_manager.filter_by_time_interval(self.current_data, self.current_period)
        if hasattr(self, '_mapped_date_range') and self._mapped_date_range:
            s, e = self._mapped_date_range
            try:
                filtered_data = filtered_data[(filtered_data['Date'] >= s) & (filtered_data['Date'] <= e)]
            except Exception:
                pass
        if filtered_data.empty:
            return pn.pane.Markdown("## No data available\n\nNo data found for the selected time period.")
        # Use legend border color from config (primary_color = #47356A)
        legend_config = plotly_legend_config("<b>Select/deselect indicator by clicking on the text</b>")
        legend_config['bordercolor'] = self.config.primary_color
        fig = self.figure_factory.create_detailed_price_figure(
            df=filtered_data,
            symbol=self.current_symbol,
            period=self.current_period,
            mapped_range=getattr(self, '_mapped_date_range', None),
            legend_config=legend_config,
            margins=standard_margins(120, 160)
        )
        return pn.pane.Plotly(fig, sizing_mode='stretch_both', config={'responsive': True})

    def _create_info_panel(self):
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("## No statistics available\n\nClick **Load Data** to load market data.")
        filtered_data = self.data_manager.filter_by_time_interval(self.current_data, self.current_period)
        if filtered_data.empty:
            return pn.pane.Markdown("## No data available\n\nNo data found for the selected time period.")
        if hasattr(self, '_mapped_date_range') and self._mapped_date_range:
            s, e = self._mapped_date_range
            try:
                filtered_data = filtered_data[(filtered_data['Date'] >= s) & (filtered_data['Date'] <= e)]
                if filtered_data.empty:
                    return pn.pane.Markdown("## No data available\n\nNo data found for the selected date range.")
            except Exception:
                pass
        if 'SMA_50' not in filtered_data.columns:
            filtered_data = self.data_manager.add_technical_indicators(filtered_data)
        period_stats = self.data_manager.calculate_period_stats(filtered_data)
        all_time_stats = self.data_manager.calculate_all_time_stats(self.current_data)
        indicators = self.data_manager.get_indicator_values(filtered_data)
        info_text = f"""
### 📊 {self.current_symbol} Statistics

**Current Price:** ${period_stats['current_price']:,.2f}

**Period Change:** {period_stats['period_change']:+.2f}%

**Period High:** ${period_stats['period_high']:,.2f}

**Period Low:** ${period_stats['period_low']:,.2f}

**All-Time High:** ${all_time_stats['ath']:,.2f}

**All-Time Low:** ${all_time_stats['atl']:,.2f}

**Avg Volume:** {period_stats['avg_volume']:,.0f}

---

### 📈 Technical Indicators
"""
        if indicators['sma_50']:
            info_text += f"\n**SMA 50:** ${indicators['sma_50']:,.2f}\n"
        if indicators['sma_200']:
            info_text += f"\n**SMA 200:** ${indicators['sma_200']:,.2f}\n"
        if indicators['ema_50']:
            info_text += f"\n**EMA 50:** ${indicators['ema_50']:,.2f}\n"
        if indicators['ema_200']:
            info_text += f"\n**EMA 200:** ${indicators['ema_200']:,.2f}\n"
        if indicators['trend']:
            if indicators['trend'] == 'bullish':
                info_text += f"\n---\n\n**Trend:** 🟢 Bullish (Golden Cross)\n"
            else:
                info_text += f"\n---\n\n**Trend:** 🔴 Bearish (Death Cross)\n"
        info_text += f"\n**Data Points:** {period_stats['data_points']:,}"
        return pn.pane.Markdown(info_text, styles=self.config.styles)

    def create_dashboard(self) -> pn.Column:
        header = create_header(self.display_name, self.config.primary_color)
        summary_box = create_summary_box(
            """
            **Quick Overview:** <br>
            <br>
            Advanced price chart with technical indicators including Simple Moving Averages (SMA) and 
            Exponential Moving Averages (EMA), combined with trading volume analysis. <br>
            <br>
            *See bottom of page for detailed indicator explanations.*
            """,
            self.config.primary_color
        )
        explanation = technical_analysis_guide()
        controls = pn.Column(
            pn.Row(self.widgets['symbol_selector'], self.widgets['period_selector'], self.widgets['range_label'], sizing_mode='stretch_width'),
            pn.Row(self.widgets['range_idx'], sizing_mode='stretch_width'),
            sizing_mode='stretch_width',
            margin=(8, 0)
        )
        self.chart_pane = pn.Column(sizing_mode='stretch_width', min_height=1200)
        self.info_pane = pn.Column(width=280, max_width=280, sizing_mode='fixed', margin=(0, 0), styles={'padding': '12px', 'background-color': self.config.light_gray_color, 'color': self.config.secondary_text_color})
        self._update_display()
        layout = pn.Column(
            header,
            summary_box,
            pn.layout.Divider(),
            controls,
            pn.layout.Divider(),
            pn.Row(self.chart_pane, self.info_pane, sizing_mode='stretch_width'),
            explanation,
            pn.layout.Divider(),
            self._create_footer_row(),
            sizing_mode='stretch_width',
            margin=(0, 0)
        )
        return layout

    def _update_display(self):
        self.chart_pane.clear()
        plotly_pane = self._create_price_chart()
        self.chart_pane.append(plotly_pane)
        try:
            if hasattr(self, '_relayout_watcher') and self._relayout_watcher is not None:
                plotly_pane.param.unwatch(self._relayout_watcher)
                self._relayout_watcher = None
            def _on_relayout(event):
                data = event.new or {}
                s = None; e = None
                if 'xaxis.range[0]' in data and 'xaxis.range[1]' in data:
                    s = data.get('xaxis.range[0]'); e = data.get('xaxis.range[1]')
                else:
                    rng = data.get('xaxis.range')
                    if isinstance(rng, (list, tuple)) and len(rng) == 2:
                        s, e = rng
                if s and e:
                    try:
                        import pandas as _pd
                        s2 = _pd.to_datetime(s).date(); e2 = _pd.to_datetime(e).date()
                        self._mapped_date_range = (s2, e2)
                        self.widgets['range_label'].object = f"#### Selected: {s2:%Y-%m-%d} → {e2:%Y-%m-%d}"
                        
                        effective_period = self._get_effective_period(s2, e2)
                        if self.current_period != effective_period:
                            self.widgets['period_selector'].value = effective_period

                    except Exception:
                        pass
            self._relayout_watcher = plotly_pane.param.watch(_on_relayout, 'relayout_data')
        except Exception:
            pass
        self.info_pane.clear()
        self.info_pane.append(self._create_info_panel())

    def refresh_data(self):
        self._load_data()
        if hasattr(self, 'chart_pane'):
            self._update_display()

    def get_dependencies(self) -> list:
        return [
            'panel>=1.3.0',
            'plotly>=5.0.0',
            'pandas>=1.3.0',
            'requests>=2.25.0',
            'python-dotenv>=0.19.0',
            'matplotlib>=3.5.0'
        ]

    # Footer provided by BaseDashboard._create_footer_row()
