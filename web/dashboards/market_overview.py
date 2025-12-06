"""
Market Overview Dashboard
Shows current price vs all-time high and price comparison for multiple cryptocurrencies.
"""

import panel as pn
import plotly.graph_objects as go
import matplotlib.colors as mcolors
import pandas as pd
from base_dashboard import BaseDashboard
from data_manager import DataManager
from config import AppConfig

class MarketOverviewDashboard(BaseDashboard):
    """Market overview dashboard for multiple cryptocurrencies."""
    
    display_name = "Market Overview"
    description = "Market overview with current vs ATH and price comparison"
    version = "2.3"
    author = "kuranez"
    
    def __init__(self):
        super().__init__()
        self.config = AppConfig()
        self.data_manager = DataManager()
        
        # Specific symbols for market overview
        self.symbols = ['BTC', 'ETH', 'BNB', 'SOL']
        self.symbols_usdt = [f"{s}USDT" for s in self.symbols]
        
        # Data storage
        self.all_data = {}
        self.ath_dict = {}
        self.current_price_dict = {}
        
        # Create widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the control widgets."""
        pass
    
    def _on_refresh_click(self, event):
        """Handle refresh button click."""
        self._load_data()
        if hasattr(self, 'plot1_pane'):
            self._update_display()
    
    def _load_data(self):
        """Load data for all symbols."""
        self.all_data = {}
        self.ath_dict = {}
        self.current_price_dict = {}
        
        try:
            for symbol, symbol_usdt in zip(self.symbols, self.symbols_usdt):
                # Fetch combined data (hourly + daily + weekly for comprehensive coverage)
                df = self.data_manager.fetch_combined_data(symbol_usdt)
                
                if not df.empty:
                    # Add symbol column
                    df['Symbol'] = symbol
                    self.all_data[symbol] = df
                    
                    # Calculate ATH and current price
                    self.ath_dict[symbol] = df['High'].max()
                    self.current_price_dict[symbol] = df['Close'].iloc[-1]
                    
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _convert_color(self, color_name, opacity=1.0):
        """Convert a color name to rgba format."""
        rgba = mcolors.to_rgba(color_name, opacity)
        return f'rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {rgba[3]})'
    
    def _create_combined_plot(self):
        """Create combined plot with price comparison and current vs ATH using shared legend."""
        if not self.all_data:
            return pn.pane.Markdown("## No data available\n\nClick **Load Data** to load market data.")
        
        from plotly.subplots import make_subplots
        
        # Create subplots: 1 row, 2 columns (side by side)
        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.55, 0.45],
            subplot_titles=("Price Comparison of Major Cryptocurrency Chains", "Current Price vs. All-Time High"),
            horizontal_spacing=0.08,
            specs=[[{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Column 1: Price comparison plot
        for symbol in self.symbols:
            if symbol not in self.all_data:
                continue
                
            df_symbol = self.all_data[symbol]
            current_price = self.current_price_dict[symbol]
            ath = self.ath_dict[symbol]
            color_a = self.config.get_crypto_color(symbol, 'primary')
            color_b = self.config.get_crypto_color(symbol, 'secondary')
            
            # Add price line with current and ATH in legend
            fig.add_trace(go.Scatter(
                x=df_symbol['Date'],
                y=df_symbol['Close'],
                mode='lines',
                name=f'{symbol} - Current: ${current_price:,.2f} | ATH: ${ath:,.2f}',
                legendgroup=symbol,
                line=dict(color=self._convert_color(color_a, 0.8)),
                fill='tozeroy',
                fillcolor=self._convert_color(color_b, 0.6),
                hovertemplate=f'{symbol}<br>Date: %{{x}}<br>Close: $ %{{y:,.2f}}<extra></extra>',
                showlegend=True
            ), row=1, col=1)
        
        # Column 2: Current vs ATH plot
        for symbol in self.symbols:
            if symbol not in self.all_data:
                continue
                
            color_a = self.config.get_crypto_color(symbol, 'primary')
            color_b = self.config.get_crypto_color(symbol, 'secondary')
            
            ath = self.ath_dict[symbol]
            current = self.current_price_dict[symbol]
            
            # ATH bar (hidden from legend)
            fig.add_trace(go.Bar(
                name=f'{symbol} ATH',
                y=[symbol],
                x=[ath],
                legendgroup=symbol,
                marker_color=self._convert_color(color_b, 0.6),
                orientation='h',
                hovertemplate=f'{symbol}<br>All-Time-High: $ %{{x:,.2f}}<extra></extra>',
                showlegend=False
            ), row=1, col=2)
            
            # Current price bar (hidden from legend)
            fig.add_trace(go.Bar(
                name=f'{symbol} Current',
                y=[symbol],
                x=[current],
                legendgroup=symbol,
                marker_color=self._convert_color(color_a, 0.8),
                orientation='h',
                hovertemplate=f'{symbol}<br>Latest Price: $ %{{x:,.2f}}<extra></extra>',
                showlegend=False
            ), row=1, col=2)
        
        # Update layout
        fig.update_xaxes(title_text="Date", row=1, col=1, rangeslider_visible=True)
        fig.update_yaxes(title_text="Price (USD)", type="log", row=1, col=1)
        fig.update_xaxes(title_text="Price (USD)", type="log", row=1, col=2)
        fig.update_yaxes(title_text="", row=1, col=2)
        
        fig.update_layout(
            barmode='overlay',
            template=self.config.get_plotly_template(),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1
            ),
            autosize=True,
            height=600,
            margin=dict(l=50, r=250, t=80, b=50)
        )
        
        return pn.pane.Plotly(fig, sizing_mode='stretch_both')
    
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
        
        # Create reactive pane for combined plot
        self.plot_pane = pn.Column(sizing_mode='stretch_both', min_height=600)
        
        # Initialize with current data
        self._update_display()
        
        # Create layout with responsive design - single combined plot
        layout = pn.Column(
            header,
            pn.layout.Divider(),
            self.plot_pane,
            sizing_mode='stretch_width',
            margin=(20, 20)
        )
        
        return layout
    
    def _update_display(self):
        """Update the plot panel."""
        # Clear and update combined plot
        self.plot_pane.clear()
        self.plot_pane.append(self._create_combined_plot())
    
    def refresh_data(self):
        """Refresh the dashboard data."""
        self._load_data()
        if hasattr(self, 'plot_pane'):
            self._update_display()
    
    def get_dependencies(self) -> list:
        """Get required dependencies."""
        return [
            'panel>=1.3.0',
            'plotly>=5.0.0',
            'pandas>=1.3.0',
            'requests>=2.25.0',
            'matplotlib>=3.5.0'
        ]
