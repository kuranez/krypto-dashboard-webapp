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
    
    def _create_current_vs_ath_plot(self):
        """Plot the current price vs All-Time High."""
        if not self.all_data:
            return pn.pane.Markdown("## No data available\n\nClick **Load Data** to load market data.")
        
        fig = go.Figure()
        
        for symbol in self.symbols:
            if symbol not in self.all_data:
                continue
                
            color_a = self.config.get_crypto_color(symbol, 'primary')
            color_b = self.config.get_crypto_color(symbol, 'secondary')
            
            ath = self.ath_dict[symbol]
            current = self.current_price_dict[symbol]
            
            # ATH bar
            fig.add_trace(go.Bar(
                name=f'{symbol} All-Time-High: $ {ath:,.2f}',
                y=[symbol],
                x=[ath],
                marker_color=self._convert_color(color_b, 0.6),
                orientation='h',
                hovertemplate=f'{symbol}<br>All-Time-High: $ %{{x:,.2f}}<extra></extra>'
            ))
            
            # Current price bar
            fig.add_trace(go.Bar(
                name=f'{symbol} Current Price: $ {current:,.2f}',
                y=[symbol],
                x=[current],
                marker_color=self._convert_color(color_a, 0.8),
                orientation='h',
                hovertemplate=f'{symbol}<br>Latest Price: $ %{{x:,.2f}}<extra></extra>'
            ))
        
        fig.update_layout(
            title_text="Current Price vs. All-Time High",
            xaxis_title="Price (USD)",
            barmode='overlay',
            xaxis_type='log',
            template=self.config.get_plotly_template(),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            autosize=True,
            margin=dict(l=50, r=150, t=50, b=50)
        )
        
        return pn.pane.Plotly(fig, sizing_mode='stretch_both')
    
    def _create_price_comparison_plot(self):
        """Plot the price curves over time for all symbols."""
        if not self.all_data:
            return pn.pane.Markdown("## No data available\n\nClick **Load Data** to load market data.")
        
        fig = go.Figure()
        
        for symbol in self.symbols:
            if symbol not in self.all_data:
                continue
                
            df_symbol = self.all_data[symbol]
            color_a = self.config.get_crypto_color(symbol, 'primary')
            color_b = self.config.get_crypto_color(symbol, 'secondary')
            
            fig.add_trace(go.Scatter(
                x=df_symbol['Date'],
                y=df_symbol['Close'],
                mode='lines',
                name=f'{symbol} Close',
                line=dict(color=self._convert_color(color_a, 0.8)),
                fill='tozeroy',
                fillcolor=self._convert_color(color_b, 0.6),
                hovertemplate=f'{symbol}<br>Date: %{{x}}<br>Close: $ %{{y:,.2f}}<extra></extra>'
            ))
        
        fig.update_layout(
            title_text="Price Comparison of Major Cryptocurrency Chains",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            yaxis_type="log",
            xaxis_rangeslider_visible=True,
            template=self.config.get_plotly_template(),
            showlegend=True,
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5
            ),
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=50)
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
        
        # Create reactive panes that can be updated
        self.plot1_pane = pn.Column(sizing_mode='stretch_both', min_height=500)
        self.plot2_pane = pn.Column(sizing_mode='stretch_both', min_height=500)
        
        # Initialize with current data
        self._update_display()
        
        # Create layout with responsive design - plots in a row (plot2 then plot1)
        layout = pn.Column(
            header,
            pn.layout.Divider(),
            pn.Row(
                self.plot2_pane,
                self.plot1_pane,
                sizing_mode='stretch_width'
            ),
            sizing_mode='stretch_width',
            margin=(20, 20)
        )
        
        return layout
    
    def _update_display(self):
        """Update the plot panels."""
        # Clear and update plot 1
        self.plot1_pane.clear()
        self.plot1_pane.append(self._create_current_vs_ath_plot())
        
        # Clear and update plot 2
        self.plot2_pane.clear()
        self.plot2_pane.append(self._create_price_comparison_plot())
    
    def refresh_data(self):
        """Refresh the dashboard data."""
        self._load_data()
        if hasattr(self, 'plot1_pane'):
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
