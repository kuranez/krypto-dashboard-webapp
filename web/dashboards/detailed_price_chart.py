"""
Detailed Price Chart Dashboard
A detailed dashboard showing price chart with technical indicators and volume.
"""

import panel as pn
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from base_dashboard import BaseDashboard
from data_manager import DataManager
from figure_factory import FigureFactory
from config import AppConfig

class DetailedPriceDashboard(BaseDashboard):
    """Detailed dashboard with price chart, technical indicators, and volume."""
    
    display_name = "Detailed Price Chart"
    description = "Detailed price chart with SMA/EMA indicators and volume"
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
        
        # Bind events
        self.widgets['symbol_selector'].param.watch(self._on_symbol_change, 'value')
        self.widgets['period_selector'].param.watch(self._on_period_change, 'value')
    
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
        """Create the detailed price chart with technical indicators and volume."""
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("## No data available\n\nClick **Load Data** to load market data.")
        
        # Filter data by time period
        filtered_data = self.data_manager.filter_by_time_interval(
            self.current_data, 
            self.current_period
        )
        
        if filtered_data.empty:
            return pn.pane.Markdown("## No data available\n\nNo data found for the selected time period.")
        
        # Calculate moving averages if not present
        df = filtered_data.copy()
        if 'SMA_50' not in df.columns:
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
        if 'SMA_200' not in df.columns:
            df['SMA_200'] = df['Close'].rolling(window=200).mean()
        if 'EMA_50' not in df.columns:
            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        if 'EMA_200' not in df.columns:
            df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
        
        # Get crypto-specific colors
        primary_color = self.config.get_crypto_color(self.current_symbol, 'primary')
        secondary_color = self.config.get_crypto_color(self.current_symbol, 'secondary')
        
        # Convert matplotlib colors to rgba
        import matplotlib.colors as mcolors
        
        def to_rgba(color_name, opacity=1.0):
            rgba = mcolors.to_rgba(color_name, opacity)
            return f'rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {rgba[3]})'
        
        color_a = to_rgba(primary_color, 0.8)
        color_b = to_rgba(secondary_color, 0.6)
        
        # Create subplots - price chart and volume
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=[0.8, 0.2],
            subplot_titles=(f'{self.current_symbol} Price Chart ({self.current_period})', 'Trading Volume')
        )
        
        # Update subplot title font sizes and move them down to create space for legend
        for annotation in fig.layout.annotations:
            annotation.update(
                font=dict(size=18, color='#47356A'),
                y=annotation.y + 0.03  # Move subtitle up to create more space
            )
        
        # Price traces - High, Low, Close using crypto colors
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['High'],
                mode='lines',
                name='High',
                line=dict(color=to_rgba(primary_color, 0.4), width=1),
                hovertemplate='<b>High</b>: <b>$%{y:,.2f}</b><extra></extra>'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Low'],
                mode='lines',
                name='Low',
                line=dict(color=to_rgba(secondary_color, 0.4), width=1),
                hovertemplate='<b>Low</b>: <b>$%{y:,.2f}</b><extra></extra>'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Close'],
                mode='lines',
                name='Close',
                line=dict(color=color_a, width=2),
                hovertemplate='<b>Close</b>: <b>$%{y:,.2f}</b><extra></extra>'
            ),
            row=1, col=1
        )
        
        # SMA traces
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['SMA_50'],
                mode='lines',
                name='SMA 50',
                line=dict(color='rgba(231, 76, 60, 0.8)', width=1.5, dash='dash'),
                hovertemplate='<b>SMA 50</b>: <b>$%{y:,.2f}</b><extra></extra>'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['SMA_200'],
                mode='lines',
                name='SMA 200',
                line=dict(color='rgba(155, 89, 182, 0.8)', width=1.5, dash='dash'),
                hovertemplate='<b>SMA 200</b>: <b>$%{y:,.2f}</b><extra></extra>'
            ),
            row=1, col=1
        )
        
        # EMA traces
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['EMA_50'],
                mode='lines',
                name='EMA 50',
                line=dict(color='rgba(243, 156, 18, 0.8)', width=1.5, dash='dot'),
                hovertemplate='<b>EMA 50</b>: <b>$%{y:,.2f}</b><extra></extra>'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['EMA_200'],
                mode='lines',
                name='EMA 200',
                line=dict(color='rgba(26, 188, 156, 0.8)', width=1.5, dash='dot'),
                hovertemplate='<b>EMA 200</b>: <b>$%{y:,.2f}</b><extra></extra>'
            ),
            row=1, col=1
        )
        
        # Prepare volume data - aggregate by week/month for larger time periods
        # Determine aggregation period based on selected time period
        if self.current_period in ['2Y', '3Y', '5Y', 'All_Time']:
            # For very long periods (2Y+), aggregate by month
            df_copy = df.copy()
            df_copy['Month'] = df_copy['Date'].dt.to_period('M').apply(lambda r: r.start_time)
            df_volume = df_copy.groupby('Month').agg({
                'Volume': 'sum',
                'Close': 'last',
                'Open': 'first'
            }).reset_index()
            df_volume.rename(columns={'Month': 'Date'}, inplace=True)
        elif self.current_period in ['3M', '6M', '1Y']:
            # For medium periods (3M-1Y), aggregate by week
            df_copy = df.copy()
            df_copy['Week'] = df_copy['Date'].dt.to_period('W').apply(lambda r: r.start_time)
            df_volume = df_copy.groupby('Week').agg({
                'Volume': 'sum',
                'Close': 'last',
                'Open': 'first'
            }).reset_index()
            df_volume.rename(columns={'Week': 'Date'}, inplace=True)
        else:
            # For shorter periods (1D, 1W, 1M), aggregate by day
            df_volume = df.groupby('Date').agg({
                'Volume': 'sum',
                'Close': 'last',
                'Open': 'first'
            }).reset_index()
        
        # Volume trace - using green for up, red for down (matching SMA/EMA colors)
        colors = ['rgba(26, 188, 156, 0.8)' if close >= open_ else 'rgba(231, 76, 60, 0.8)'
                  for close, open_ in zip(df_volume['Close'], df_volume['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=df_volume['Date'],
                y=df_volume['Volume'],
                name='Volume',
                marker_color=colors,
                hovertemplate='Volume: <b>%{y:,.0f}</b><extra></extra>'
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            template=self.config.get_plotly_template(),
            hovermode='x unified',
            hoverlabel=dict(font_size=14),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.15,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="rgba(71, 53, 106, 0.3)",
                borderwidth=1,
                font=dict(size=18),
                title=dict(
                    text="<b>Select/deselect indicator by clicking on the text</b>",
                    font=dict(size=14, color="#47356A"),
                    side="top"
                ),
                itemsizing="constant",
                tracegroupgap=15
            ),
            xaxis2_title="Date",
            yaxis_title="Price (USD)",
            yaxis2_title="Volume",
            xaxis_rangeslider_visible=False,
            autosize=True,
            # Normalize chart padding while preserving generous legend space
            margin=dict(l=24, r=24, t=120, b=160)
        )
        
        # Update axes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        
        # Format volume y-axis with better readability
        fig.update_yaxes(row=2, col=1, tickformat='.2s')
        
        return pn.pane.Plotly(fig, sizing_mode='stretch_both', config={'responsive': True})
    
    def _create_info_panel(self):
        """Create an information panel with current stats and indicators."""
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("## No statistics available\n\nClick **Load Data** to load market data.")
        
        # Filter data by time period
        filtered_data = self.data_manager.filter_by_time_interval(
            self.current_data, 
            self.current_period
        )
        
        if filtered_data.empty:
            return pn.pane.Markdown("## No data available\n\nNo data found for the selected time period.")
        
        # Add technical indicators to DataFrame if not present
        if 'SMA_50' not in filtered_data.columns:
            filtered_data = self.data_manager.add_technical_indicators(filtered_data)
        
        # Get statistics and indicator values from data manager
        period_stats = self.data_manager.calculate_period_stats(filtered_data)
        all_time_stats = self.data_manager.calculate_all_time_stats(self.current_data)
        indicators = self.data_manager.get_indicator_values(filtered_data)
        
        # Format the information
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
        
        # Add trend signal
        if indicators['trend']:
            if indicators['trend'] == 'bullish':
                info_text += f"\n---\n\n**Trend:** 🟢 Bullish (Golden Cross)\n"
            else:
                info_text += f"\n---\n\n**Trend:** 🔴 Bearish (Death Cross)\n"
        
        info_text += f"\n**Data Points:** {period_stats['data_points']:,}"
        
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
            Advanced price chart with technical indicators including Simple Moving Averages (SMA) and 
            Exponential Moving Averages (EMA), combined with trading volume analysis. <br>
            <br>
            *See bottom of page for detailed indicator explanations.*
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
        
        # Detailed explanation
        explanation = pn.pane.Markdown(
            """
            ## Technical Analysis Guide
            
            This dashboard provides comprehensive technical analysis tools for cryptocurrency price movements.
            
            **Chart Components:**
            - **Price Chart (Top)**: Historical price data with High, Low, and Close values
            - **Volume Chart (Bottom)**: Trading volume aggregated by day, week, or month depending on time period
            
            ---
            
            **Understanding Technical Indicators:**
            
            **Simple Moving Average (SMA):** Average price over a specific period
            - **SMA 50**: 50-period moving average - short to medium-term trend indicator
            - **SMA 200**: 200-period moving average - long-term trend indicator
            - **Golden Cross**: When SMA 50 crosses above SMA 200 (bullish signal 🟢)
            - **Death Cross**: When SMA 50 crosses below SMA 200 (bearish signal 🔴)
            
            **Exponential Moving Average (EMA):** Weighted average giving more importance to recent prices
            - **EMA 50**: More responsive to recent price changes than SMA 50
            - **EMA 200**: Faster-reacting long-term trend indicator than SMA 200
            - EMAs respond more quickly to price changes, making them useful for identifying trend changes earlier
            
            **Volume Analysis:**
            - **Green bars**: Price closed higher than it opened (bullish)
            - **Red/Other bars**: Price closed lower than it opened (bearish)
            - **High volume + price increase**: Strong buying pressure
            - **High volume + price decrease**: Strong selling pressure
            - Volume aggregation varies by timeframe:
              - Short periods (1D-1M): Daily volume
              - Medium periods (3M-1Y): Weekly volume
              - Long periods (2Y+): Monthly volume
            
            *Use these indicators together to make informed trading decisions. Always do your own research.*
            """,
            styles={
                'font-size': '16px',
                'background-color': '#47356A',
                'color': 'white',
                'padding': '20px',
                'border-radius': '4px',
                'margin-top': '10px'
            },
            sizing_mode='stretch_width'
        )
        
        # Controls row
        controls = pn.Row(
            self.widgets['symbol_selector'],
            self.widgets['period_selector'],
            sizing_mode='stretch_width',
            margin=(8, 0)
        )
        
        # Create reactive panes that can be updated
        self.chart_pane = pn.Column(sizing_mode='stretch_width', min_height=1200)
        self.info_pane = pn.Column(width=280, max_width=280, sizing_mode='fixed', margin=(0, 0), styles={'padding': '12px'})

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
            explanation,
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
