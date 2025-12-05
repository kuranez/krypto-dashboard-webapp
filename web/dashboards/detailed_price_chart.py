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
    version = "2.0"
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
        self.available_periods = ['1W', '1M', '3M', '6M', '1Y', 'All_Time']
        
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
        
        self.widgets['refresh_button'] = pn.widgets.Button(
            name='Refresh Data',
            button_type='primary',
            width=120,
            margin=(5, 10)
        )
        
        # Bind events
        self.widgets['symbol_selector'].param.watch(self._on_symbol_change, 'value')
        self.widgets['period_selector'].param.watch(self._on_period_change, 'value')
        self.widgets['refresh_button'].on_click(self._on_refresh_click)
    
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
            # Fetch historical data
            df = self.data_manager.fetch_historical_data(symbol=symbol_usdt, limit=1000)
            
            if not df.empty:
                self.current_data = df
            else:
                self.current_data = None
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.current_data = None
    
    def _create_price_chart(self):
        """Create the detailed price chart with technical indicators and volume."""
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("No data to display")
        
        # Filter data by time period
        filtered_data = self.data_manager.filter_by_time_interval(
            self.current_data, 
            self.current_period
        )
        
        if filtered_data.empty:
            return pn.pane.Markdown("No data available for selected time period")
        
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
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3],
            subplot_titles=(f'{self.current_symbol} Price Chart ({self.current_period})', 'Volume')
        )
        
        # Price traces - High, Low, Close using crypto colors
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['High'],
                mode='lines',
                name='High',
                line=dict(color=to_rgba(primary_color, 0.4), width=1),
                hovertemplate='High: $%{y:,.2f}<extra></extra>'
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
                hovertemplate='Low: $%{y:,.2f}<extra></extra>'
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
                hovertemplate='Close: $%{y:,.2f}<extra></extra>'
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
                hovertemplate='SMA 50: $%{y:,.2f}<extra></extra>'
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
                hovertemplate='SMA 200: $%{y:,.2f}<extra></extra>'
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
                hovertemplate='EMA 50: $%{y:,.2f}<extra></extra>'
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
                hovertemplate='EMA 200: $%{y:,.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Volume trace - using crypto colors
        colors = [to_rgba(primary_color, 0.6) if close >= open_ else to_rgba(secondary_color, 0.4)
                  for close, open_ in zip(df['Close'], df['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=df['Date'],
                y=df['Volume'],
                name='Volume',
                marker_color=colors,
                hovertemplate='Volume: %{y:,.0f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            template=self.config.get_plotly_template(),
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5
            ),
            xaxis2_title="Date",
            yaxis_title="Price (USD)",
            yaxis2_title="Volume",
            xaxis_rangeslider_visible=True,
            autosize=True,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Update axes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        
        return pn.pane.Plotly(fig, sizing_mode='stretch_both')
    
    def _create_info_panel(self):
        """Create an information panel with current stats and indicators."""
        if self.current_data is None or self.current_data.empty:
            return pn.pane.Markdown("No statistics available")
        
        # Filter data by time period
        filtered_data = self.data_manager.filter_by_time_interval(
            self.current_data, 
            self.current_period
        )
        
        if filtered_data.empty:
            return pn.pane.Markdown("No data available")
        
        # Calculate statistics
        latest_price = filtered_data['Close'].iloc[-1]
        price_change = (
            (filtered_data['Close'].iloc[-1] - filtered_data['Close'].iloc[0]) 
            / filtered_data['Close'].iloc[0] * 100
        ) if len(filtered_data) > 1 else 0
        
        high_price = filtered_data['High'].max()
        low_price = filtered_data['Low'].min()
        avg_volume = filtered_data['Volume'].mean()
        
        # Calculate moving averages
        sma_50 = filtered_data['Close'].rolling(window=50).mean().iloc[-1] if len(filtered_data) >= 50 else None
        sma_200 = filtered_data['Close'].rolling(window=200).mean().iloc[-1] if len(filtered_data) >= 200 else None
        ema_50 = filtered_data['Close'].ewm(span=50, adjust=False).mean().iloc[-1] if len(filtered_data) >= 50 else None
        ema_200 = filtered_data['Close'].ewm(span=200, adjust=False).mean().iloc[-1] if len(filtered_data) >= 200 else None
        
        # Format the information
        info_text = f"""
### 📊 {self.current_symbol} Statistics

**Current Price:** ${latest_price:,.2f}

**Period Change:** {price_change:+.2f}%

**Period High:** ${high_price:,.2f}

**Period Low:** ${low_price:,.2f}

**Avg Volume:** {avg_volume:,.0f}

---

### 📈 Technical Indicators
"""
        
        if sma_50:
            info_text += f"\n**SMA 50:** ${sma_50:,.2f}\n"
        if sma_200:
            info_text += f"\n**SMA 200:** ${sma_200:,.2f}\n"
        if ema_50:
            info_text += f"\n**EMA 50:** ${ema_50:,.2f}\n"
        if ema_200:
            info_text += f"\n**EMA 200:** ${ema_200:,.2f}\n"
        
        # Add trend signal
        if sma_50 and sma_200:
            if sma_50 > sma_200:
                info_text += f"\n---\n\n**Trend:** 🟢 Bullish (Golden Cross)\n"
            else:
                info_text += f"\n---\n\n**Trend:** 🔴 Bearish (Death Cross)\n"
        
        info_text += f"\n**Data Points:** {len(filtered_data):,}"
        
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
        
        # Controls row
        controls = pn.Row(
            self.widgets['symbol_selector'],
            self.widgets['period_selector'],
            self.widgets['refresh_button'],
            sizing_mode='stretch_width',
            margin=(10, 0)
        )
        
        # Create reactive panes that can be updated
        self.chart_pane = pn.Column(min_height=700)
        self.info_pane = pn.Column(sizing_mode='stretch_width')

        # Initialize with current data
        self._update_display()
        
        # Create layout with responsive design
        layout = pn.Column(
            header,
            pn.layout.Divider(),
            controls,
            pn.layout.Divider(),
            pn.Row(
            # Chart column - stretch to take all available space
            pn.Column(self.chart_pane, sizing_mode='stretch_both'),
            # Info column - keep small fixed/min width
            pn.Column(self.info_pane, sizing_mode='fixed', width=300, min_width=200),
            sizing_mode='stretch_width',
            ),
            sizing_mode='stretch_width',
            margin=(20, 20)
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
