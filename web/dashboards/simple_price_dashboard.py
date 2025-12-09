"""
Simple Price Dashboard
A basic dashboard showing just a price chart for one cryptocurrency.
"""

import panel as pn
from components.widgets import create_symbol_selector, create_period_selector, create_range_widgets
from components.layouts import standard_margins
from components.ui import create_header, create_summary_box
from base_dashboard import BaseDashboard
from data_manager import DataManager
from figure_factory import FigureFactory
from config import AppConfig

class SimplePriceDashboard(BaseDashboard):
    """Simple dashboard with one price chart for one symbol."""
    
    display_name = "Simple Price Chart"
    description = "Basic price chart for a single cryptocurrency"
    version = "2.5"
    author = "kuranez"
    
    def __init__(self):
        super().__init__()
        self.config = AppConfig()
        self.data_manager = DataManager()
        self.figure_factory = FigureFactory()
        
        # Dashboard state
        self.current_symbol = 'BTC'
        self.current_period = '1Y'
        self.current_chart_type = 'Line'
        
        # Available options
        self.available_symbols = ['BTC', 'ETH', 'BNB', 'TRX', 'SOL', 'ADA', 'DOT', 'UNI', 'XRP', 'XLM', 'LINK', 'LTC', 'DOGE', 'SHIB', 'HBAR']
        self.available_periods = list(self.config.time_intervals.keys())
        
        # Data storage
        self.current_data = None
        
        # Create widgets
        self._create_widgets()
        
        # Don't load data on startup to avoid blocking - user can click Fetch Data button
        # This makes the app responsive even without internet connection
    
    def _create_widgets(self):
        """Create the control widgets."""
        self.widgets['symbol_selector'] = create_symbol_selector(self.available_symbols, self.current_symbol)
        
        self.widgets['period_selector'] = create_period_selector(self.available_periods, self.current_period)
        
        # self.widgets['chart_type'] = pn.widgets.Select(
        #     name='Chart Type',
        #     options=['Line', 'Candlestick', 'Volume'],
        #     value=self.current_chart_type,
        #     width=150,
        #     margin=(5, 10)
        # )
        
        # Index-based range slider for consistent precision
        self.widgets['range_idx'], self.widgets['range_label'] = create_range_widgets()
        
        # Bind events
        self.widgets['symbol_selector'].param.watch(self._on_symbol_change, 'value')
        self.widgets['period_selector'].param.watch(self._on_period_change, 'value')
        # self.widgets['chart_type'].param.watch(self._on_chart_type_change, 'value')
        self.widgets['range_idx'].param.watch(self._on_range_idx_change, 'value')
    
    def _on_symbol_change(self, event):
        """Handle symbol change."""
        self.current_symbol = event.new
        self._load_data()
        if hasattr(self, 'chart_pane'):
            self._update_display()
    
    def _on_period_change(self, event):
        """Handle time period change."""
        self.current_period = event.new
        # Reset index-based slider to match selected period and update label
        if self.current_data is not None and not self.current_data.empty:
            try:
                period_df = self.data_manager.filter_by_time_interval(self.current_data, self.current_period)
                if not period_df.empty:
                    n = len(period_df)
                    self.widgets['range_idx'].start = 0
                    self.widgets['range_idx'].end = max(1, n - 1)
                    self.widgets['range_idx'].value = (0, max(1, n - 1))
                    self.widgets['range_idx'].disabled = False
                    # Map full period indices to dates and update label immediately
                    self._mapped_date_range = (period_df.iloc[0]['Date'], period_df.iloc[n - 1]['Date'])
                    self.widgets['range_label'].object = f"#### Selected: {period_df.iloc[0]['Date']:%Y-%m-%d} → {period_df.iloc[n-1]['Date']:%Y-%m-%d}"
                else:
                    self.widgets['range_idx'].start = 0
                    self.widgets['range_idx'].end = 1
                    self.widgets['range_idx'].value = (0, 1)
                    self.widgets['range_idx'].disabled = True
            except Exception:
                pass
        if hasattr(self, 'chart_pane'):
            self._update_display()
    
    def _on_range_idx_change(self, event):
        """Map index range to dates and update chart."""
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
        except Exception:
            pass
        if hasattr(self, 'chart_pane'):
            self._update_display()
    
    def _on_chart_type_change(self, event):
        """Handle chart type change."""
        self.current_chart_type = event.new
        if hasattr(self, 'chart_pane'):
            self._update_display()
        
    def _on_refresh_click(self, event):
        """Handle refresh button click."""
        self._load_data()
        if hasattr(self, 'chart_pane'):
            self._update_display()
    
    def _load_initial_data(self):
        """Load initial data for default symbol."""
        try:
            self._load_data()
        except Exception as e:
            print(f"⚠️ Could not load initial data: {e}")
            print("   Dashboard will work once you can connect to the API")
            self.current_data = None
    
    def _load_data(self):
        """Load data for the selected symbol."""
        symbol_usdt = f"{self.current_symbol}USDT"
        
        try:
            # Fetch combined data (hourly + daily for comprehensive coverage)
            df = self.data_manager.fetch_combined_data(symbol=symbol_usdt)
            
            if not df.empty:
                # Filter false ATH spikes (data errors)
                df = self.data_manager.filter_price_spikes(df, spike_threshold=4.0)
                self.current_data = df
            else:
                self.current_data = None
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.current_data = None
        
        # Initialize index range slider when data is available
        if self.current_data is not None and not self.current_data.empty:
            date_min = self.current_data['Date'].min()
            date_max = self.current_data['Date'].max()
            # Default slider bounds to the selected period, not full dataset
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
        """Create the main price chart based on selected chart type."""
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("## No data available\n\nClick **Load Data** to load market data.")
        
        # Filter data by time period
        filtered_data = self.data_manager.filter_by_time_interval(
            self.current_data, 
            self.current_period
        )
        
        # Apply mapped index-based date range if present
        if hasattr(self, '_mapped_date_range') and self._mapped_date_range:
            start_date, end_date = self._mapped_date_range
            try:
                filtered_data = filtered_data[(filtered_data['Date'] >= start_date) & (filtered_data['Date'] <= end_date)]
            except Exception:
                pass

        # Ensure plotted area reflects selected date range
        x_range = None
        if hasattr(self, '_mapped_date_range') and self._mapped_date_range:
            x_range = self._mapped_date_range
        
        if filtered_data.empty:
            return pn.pane.Markdown("## No data available\n\nNo data found for the selected time period.")
        
        # Create the chart based on type using FigureFactory
        
        if self.current_chart_type == 'Line':
            title = f"{self.current_symbol} Price Chart ({self.current_period})"
            fig = self.figure_factory.create_simple_price_chart(
                filtered_data, 
                self.current_symbol, 
                title
            )
            # Standardize font sizes
            fig.update_layout(
                title_font_size=18,
                hoverlabel=dict(font_size=14)
            )
            if x_range:
                fig.update_xaxes(range=x_range)
        elif self.current_chart_type == 'Candlestick':
            fig = self.figure_factory.create_candlestick(
                filtered_data,
                title=f"{self.current_symbol} Candlestick Chart ({self.current_period})",
                x_range=x_range,
                margins=standard_margins(140, 180)
            )
        elif self.current_chart_type == 'Volume':
            fig = self.figure_factory.create_volume_only(
                filtered_data,
                title=f"{self.current_symbol} Trading Volume ({self.current_period})",
                x_range=x_range,
                margins=standard_margins(140, 180)
            )
        
        return pn.pane.Plotly(fig, sizing_mode='stretch_both')
    
    def _create_info_panel(self):
        """Create an information panel with current stats."""
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("No statistics available")
        
        # Filter data by current period
        filtered_data = self.data_manager.filter_by_time_interval(
            self.current_data, 
            self.current_period
        )
        
        # Apply mapped index-based date range if set
        if hasattr(self, '_mapped_date_range') and self._mapped_date_range:
            start_date, end_date = self._mapped_date_range
            try:
                filtered_data = filtered_data[(filtered_data['Date'] >= start_date) & (filtered_data['Date'] <= end_date)]
            except Exception:
                pass
        
        # Get all-time statistics from data manager
        stats = self.data_manager.calculate_all_time_stats(self.current_data)
        
        # Get period statistics if filtered data is available
        if not filtered_data.empty:
            period_stats = self.data_manager.calculate_period_stats(filtered_data)
            period_high = period_stats['period_high']
            period_low = period_stats['period_low']
        else:
            period_high = stats['ath']
            period_low = stats['atl']
        
        # Format the information
        info_text = f"""
        ### 📊 {self.current_symbol} Statistics
        
        **Current Price:** ${stats['current_price']:,.2f}
        
        **24h Change:** {stats['price_change_24h']:+.2f}%
        
        **Period High:** ${period_high:,.2f}
        
        **Period Low:** ${period_low:,.2f}
        
        **All-Time High:** ${stats['ath']:,.2f}
        
        **All-Time Low:** ${stats['atl']:,.2f}
        
        **Data Points:** {len(self.current_data):,}
        """
        
        return pn.pane.Markdown(info_text, styles=self.config.styles)
    
    def create_dashboard(self) -> pn.Column:
        """Create and return the dashboard layout."""
        
        # Header
        header = create_header(self.display_name, self.config.primary_color)
        
        # Quick summary box
        summary_box = create_summary_box(
            """
            **Quick Overview:** <br>
            <br>
            Track individual cryptocurrency price movements over time.
            Select your preferred cryptocurrency and time period to view historical price trends.
            """,
            self.config.primary_color
        )
        
        # Controls: first row (selectors + range label), second row (slider)
        controls = pn.Column(
            pn.Row(
                self.widgets['symbol_selector'],
                self.widgets['period_selector'],
                self.widgets['range_label'],
                sizing_mode='stretch_width'
            ),
            pn.Row(
                self.widgets['range_idx'],
                sizing_mode='stretch_width'
            ),
            sizing_mode='stretch_width',
            margin=(8, 0)
        )
        
        # Create reactive panes that can be updated
        self.chart_pane = pn.Column(sizing_mode='stretch_both', min_height=500)
        self.info_pane = pn.Column(width=280, max_width=280, sizing_mode='fixed', styles={'padding': '12px', 'background-color': self.config.light_gray_color, 'color': self.config.secondary_text_color})

        # Initialize with current data
        self._update_display()
        
        # Create layout with responsive design
        layout = pn.Column(
            header,
            summary_box,
            pn.layout.Divider(),
            controls,
            pn.layout.Divider(),
            pn.Row(
                self.chart_pane,
                self.info_pane,
                sizing_mode='stretch_width'
            ),
            pn.layout.Divider(),
            self._create_footer_row(),
            sizing_mode='stretch_width',
            margin=(0, 0)
        )
        
        return layout
    
    def _update_display(self):
        """Update the chart and info panels."""
        # Clear and update chart
        self.chart_pane.clear()
        plotly_pane = self._create_price_chart()
        self.chart_pane.append(plotly_pane)
        
        # Link Plotly zoom (relayout) back to index label/mapped dates
        try:
            # Remove previous watcher if exists
            if hasattr(self, '_relayout_watcher') and self._relayout_watcher is not None:
                plotly_pane.param.unwatch(self._relayout_watcher)
                self._relayout_watcher = None
            
            def _on_relayout(event):
                data = event.new or {}
                # Plotly may emit xaxis.range[0]/[1] or xaxis.range
                start = None
                end = None
                if 'xaxis.range[0]' in data and 'xaxis.range[1]' in data:
                    start = data.get('xaxis.range[0]')
                    end = data.get('xaxis.range[1]')
                else:
                    rng = data.get('xaxis.range')
                    if isinstance(rng, (list, tuple)) and len(rng) == 2:
                        start, end = rng
                
                # Update mapped range/label if values parsed
                if start and end:
                    try:
                        import pandas as _pd
                        s = _pd.to_datetime(start).date()
                        e = _pd.to_datetime(end).date()
                        self._mapped_date_range = (s, e)
                        self.widgets['range_label'].object = f"#### Selected: {s:%Y-%m-%d} → {e:%Y-%m-%d}"
                    except Exception:
                        pass
            
            self._relayout_watcher = plotly_pane.param.watch(_on_relayout, 'relayout_data')
        except Exception:
            pass
        
        # Clear and update info
        self.info_pane.clear()
        self.info_pane.append(self._create_info_panel())
    
    def refresh_data(self):
        """Refresh the dashboard data."""
        self._load_data()
        if hasattr(self, 'chart_pane'):
            self._update_display()
    
    def get_dependencies(self) -> list:
        """Get required dependencies."""
        return [
            'panel>=1.3.0',
            'plotly>=5.0.0',
            'pandas>=1.3.0',
            'requests>=2.25.0',
            'python-dotenv>=0.19.0',
            'matplotlib>=3.5.0'
        ]

    # Footer is provided by BaseDashboard._create_footer_row()
