"""
Simple Price Dashboard
A basic dashboard showing just a price chart for one cryptocurrency.
"""

import panel as pn
from base_dashboard import BaseDashboard
from data_manager import DataManager
from figure_factory import FigureFactory
from config import AppConfig

class SimplePriceDashboard(BaseDashboard):
    """Simple dashboard with one price chart for one symbol."""
    
    display_name = "Simple Price Chart"
    description = "Basic price chart for a single cryptocurrency"
    version = "2.3"
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
        self.widgets['symbol_selector'] = pn.widgets.Select(
            name='Select Cryptocurrency',
            options=self.available_symbols,
            value=self.current_symbol,
            width=200,
            margin=(5, 10)
        )
        
        self.widgets['period_selector'] = pn.widgets.Select(
            name='Time Period',
            options=self.available_periods,
            value=self.current_period,
            width=150,
            margin=(5, 10)
        )
        
        # self.widgets['chart_type'] = pn.widgets.Select(
        #     name='Chart Type',
        #     options=['Line', 'Candlestick', 'Volume'],
        #     value=self.current_chart_type,
        #     width=150,
        #     margin=(5, 10)
        # )
        
        # Bind events
        self.widgets['symbol_selector'].param.watch(self._on_symbol_change, 'value')
        self.widgets['period_selector'].param.watch(self._on_period_change, 'value')
        # self.widgets['chart_type'].param.watch(self._on_chart_type_change, 'value')
    
    def _on_symbol_change(self, event):
        """Handle symbol change."""
        self.current_symbol = event.new
        self._load_data()
        if hasattr(self, 'chart_pane'):
            self._update_display()
    
    def _on_period_change(self, event):
        """Handle time period change."""
        self.current_period = event.new
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
    
    def _create_price_chart(self):
        """Create the main price chart based on selected chart type."""
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("## No data available\n\nClick **Load Data** to load market data.")
        
        # Filter data by time period
        filtered_data = self.data_manager.filter_by_time_interval(
            self.current_data, 
            self.current_period
        )
        
        if filtered_data.empty:
            return pn.pane.Markdown("## No data available\n\nNo data found for the selected time period.")
        
        # Create the chart based on type
        import plotly.graph_objects as go
        
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
        elif self.current_chart_type == 'Candlestick':
            fig = go.Figure(data=[go.Candlestick(
                x=filtered_data['Date'],
                open=filtered_data['Open'],
                high=filtered_data['High'],
                low=filtered_data['Low'],
                close=filtered_data['Close']
            )])
            fig.update_layout(
                title=f"{self.current_symbol} Candlestick Chart ({self.current_period})",
                title_font_size=18,
                hoverlabel=dict(font_size=14),
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                template=self.config.get_plotly_template(),
                xaxis_rangeslider_visible=True,
                autosize=True,
                margin=dict(l=50, r=50, t=50, b=50)
            )
        elif self.current_chart_type == 'Volume':
            fig = go.Figure(data=[go.Bar(
                x=filtered_data['Date'],
                y=filtered_data['Volume'],
                marker_color='#3498db'
            )])
            fig.update_layout(
                title=f"{self.current_symbol} Trading Volume ({self.current_period})",
                title_font_size=18,
                hoverlabel=dict(font_size=14),
                xaxis_title="Date",
                yaxis_title="Volume",
                template=self.config.get_plotly_template(),
                autosize=True,
                margin=dict(l=50, r=50, t=50, b=50)
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
        header = pn.pane.Markdown(
            f"## {self.display_name}",
            styles={
                'font-size': '24px', 
                'color': self.config.primary_color,
                'text-align': 'center'
            }
        )
        
        # Quick summary box
        summary_box = pn.pane.Markdown(
            """
            **Quick Overview:** <br>
            <br>
            Track individual cryptocurrency price movements over time.
            Select your preferred cryptocurrency and time period to view historical price trends.
            """,
            styles={
                'font-size': '16px',
                'background-color': '#f8f9fa',
                'color': '#2c3e50',
                'padding': '12px',
                'border-radius': '5px',
                'border-left': f'4px solid {self.config.primary_color}',
                'margin': '6px 0'
            },
            sizing_mode='stretch_width'
        )
        
        # Controls row
        controls = pn.Row(
            self.widgets['symbol_selector'],
            self.widgets['period_selector'],
            # self.widgets['chart_type'],
            # sizing_mode='stretch_width',
            margin=(8, 0)
        )
        
        # Create reactive panes that can be updated
        self.chart_pane = pn.Column(sizing_mode='stretch_both', min_height=500)
        self.info_pane = pn.Column(width=280, max_width=280, sizing_mode='fixed', styles={'padding': '12px'})

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
        self.chart_pane.append(self._create_price_chart())
        
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
