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
    version = "2.4"
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
        self.correlation_dict = {}  # Latest 30-day correlation vs BTC
        self.beta_dict = {}  # Latest 30-day beta vs BTC
        self.correlation_series = {}  # Historical rolling correlation series
        self.beta_series = {}  # Historical rolling beta series
        self.high_90d_dict = {}
        self.low_90d_dict = {}
        self.high_365d_dict = {}
        self.low_365d_dict = {}
        
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
        self.correlation_dict = {}
        self.beta_dict = {}
        self.correlation_series = {}
        self.beta_series = {}
        self.high_90d_dict = {}
        self.low_90d_dict = {}
        self.high_365d_dict = {}
        self.low_365d_dict = {}
        
        try:
            # First, load BTC data as reference
            df_btc = self.data_manager.fetch_combined_data('BTCUSDT')
            if not df_btc.empty:
                # Filter false ATH spikes (data errors)
                df_btc = self.data_manager.filter_price_spikes(df_btc, spike_threshold=4.0)
                df_btc = df_btc.reset_index(drop=True)  # Reset index after filtering
                df_btc['Symbol'] = 'BTC'
                self.all_data['BTC'] = df_btc
                self.ath_dict['BTC'] = df_btc['High'].max()
                self.current_price_dict['BTC'] = df_btc['Close'].iloc[-1]
                self.correlation_dict['BTC'] = 1.0  # BTC vs BTC = 1.0
                self.beta_dict['BTC'] = 1.0  # BTC vs BTC = 1.0
                self.correlation_series['BTC'] = pd.Series([1.0] * len(df_btc), index=df_btc.index)
                self.beta_series['BTC'] = pd.Series([1.0] * len(df_btc), index=df_btc.index)
                
                # Calculate 90-day and 1-year high/low
                cutoff_90d = df_btc['Date'].max() - pd.Timedelta(days=90)
                cutoff_365d = df_btc['Date'].max() - pd.Timedelta(days=365)
                df_90d = df_btc[df_btc['Date'] >= cutoff_90d]
                df_365d = df_btc[df_btc['Date'] >= cutoff_365d]
                
                self.high_90d_dict['BTC'] = df_90d['High'].max() if not df_90d.empty else 0
                self.low_90d_dict['BTC'] = df_90d['Low'].min() if not df_90d.empty else 0
                self.high_365d_dict['BTC'] = df_365d['High'].max() if not df_365d.empty else 0
                self.low_365d_dict['BTC'] = df_365d['Low'].min() if not df_365d.empty else 0
            
            # Load other symbols and calculate correlation/beta vs BTC
            for symbol, symbol_usdt in zip(self.symbols, self.symbols_usdt):
                if symbol == 'BTC':  # Already loaded
                    continue
                    
                # Fetch combined data (hourly + daily + weekly for comprehensive coverage)
                df = self.data_manager.fetch_combined_data(symbol_usdt)
                
                if not df.empty:
                    # Filter false ATH spikes (data errors)
                    df = self.data_manager.filter_price_spikes(df, spike_threshold=4.0)
                    df = df.reset_index(drop=True)  # Reset index after filtering
                    # Add symbol column
                    df['Symbol'] = symbol
                    self.all_data[symbol] = df
                    
                    # Calculate ATH and current price
                    self.ath_dict[symbol] = df['High'].max()
                    self.current_price_dict[symbol] = df['Close'].iloc[-1]
                    
                    # Calculate 90-day and 1-year high/low
                    cutoff_90d = df['Date'].max() - pd.Timedelta(days=90)
                    cutoff_365d = df['Date'].max() - pd.Timedelta(days=365)
                    df_90d = df[df['Date'] >= cutoff_90d]
                    df_365d = df[df['Date'] >= cutoff_365d]
                    
                    self.high_90d_dict[symbol] = df_90d['High'].max() if not df_90d.empty else 0
                    self.low_90d_dict[symbol] = df_90d['Low'].min() if not df_90d.empty else 0
                    self.high_365d_dict[symbol] = df_365d['High'].max() if not df_365d.empty else 0
                    self.low_365d_dict[symbol] = df_365d['Low'].min() if not df_365d.empty else 0
                    
                    # Calculate full historical rolling correlation and beta vs BTC
                    if not df_btc.empty:
                        # Calculate historical rolling metrics (30-day window)
                        corr_series = self.data_manager.calculate_rolling_correlation(df, df_btc, window=30)
                        beta_series = self.data_manager.calculate_beta_coefficient(df, df_btc, window=30)
                        
                        self.correlation_series[symbol] = corr_series
                        self.beta_series[symbol] = beta_series
                        
                        # Get latest values
                        correlation, beta = self.data_manager.get_latest_correlation_beta(df, df_btc, window=30)
                        self.correlation_dict[symbol] = correlation
                        self.beta_dict[symbol] = beta
                    else:
                        self.correlation_dict[symbol] = 0.0
                        self.beta_dict[symbol] = 0.0
                        self.correlation_series[symbol] = pd.Series(dtype=float)
                        self.beta_series[symbol] = pd.Series(dtype=float)
                    
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _convert_color(self, color_name, opacity=1.0):
        """Convert a color name to rgba format."""
        rgba = mcolors.to_rgba(color_name, opacity)
        return f'rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {rgba[3]})'
    
    def _create_combined_plot(self):
        """Create combined plot with price comparison, current vs ATH, and rolling correlation."""
        if not self.all_data:
            return pn.pane.Markdown("## No data available\n\nClick **Load Data** to load market data.")
        
        from plotly.subplots import make_subplots
        
        # Create subplots: 2 rows, 2 columns
        # Row 1: Price comparison (left) and Current vs ATH (right)
        # Row 2: Rolling correlation (spans full width)
        fig = make_subplots(
            rows=2, cols=2,
            row_heights=[0.65, 0.35],
            column_widths=[0.55, 0.45],
            subplot_titles=(
                "Historical Price Comparison & Correlation of Major Cryptocurrency Chains with Bitcoin", 
                "Current Price vs. All-Time-High & 90-Day / 1-Year Trading Ranges",
                "Pearson Correlation Analysis - 30-Day Rolling Correlation vs BTC (Last 90 Days)",
            ),
            horizontal_spacing=0.08,
            vertical_spacing=0.15,
            specs=[
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "scatter", "colspan": 2}, None]
            ]
        )
        
        # Get BTC data for merging with correlation series
        df_btc = self.all_data.get('BTC', pd.DataFrame())
        
        # Column 1: Price comparison plot with historical correlation/beta in hover
        for symbol in self.symbols:
            if symbol not in self.all_data:
                continue
                
            df_symbol = self.all_data[symbol]
            current_price = self.current_price_dict[symbol]
            ath = self.ath_dict[symbol]
            color_a = self.config.get_crypto_color(symbol, 'primary')
            color_b = self.config.get_crypto_color(symbol, 'secondary')
            
            # Merge price data with correlation and beta series for hover info
            if symbol in self.correlation_series and not self.correlation_series[symbol].empty:
                # Align correlation/beta series with price data by index
                df_merged = df_symbol.copy()
                
                # Safely add correlation and beta using reindex to handle length mismatches
                # This will add NaN for indices that don't exist in the correlation series
                df_merged['Correlation'] = self.correlation_series[symbol].reindex(df_merged.index).fillna(0)
                df_merged['Beta'] = self.beta_series[symbol].reindex(df_merged.index).fillna(0)
                
                # Create custom hover data array
                customdata = df_merged[['Correlation', 'Beta']].values
                
                if symbol != 'BTC' and symbol in self.correlation_series and not self.correlation_series[symbol].empty:
                    hover_template = (
                        f'<b>{symbol}</b><br>'
                        f'Date: <b>%{{x}}</b><br>'
                        f'Close: <b>$ %{{y:,.2f}}</b><br>'
                        f'30d Correlation: <b>%{{customdata[0]:.3f}}</b><br>'
                        f'30d Beta: <b>%{{customdata[1]:.3f}}</b>'
                        '<extra></extra>'
                    )
                else:
                    # For BTC or if data is missing, use a simpler template
                    customdata = None
                    hover_template = (
                        f'<b>{symbol}</b><br>'
                        f'Date: <b>%{{x}}</b><br>'
                        f'Close: <b>$ %{{y:,.2f}}</b>'
                        '<extra></extra>'
                    )
            else:
                customdata = None
                hover_template = (
                    f'<b>{symbol}</b><br>'
                    f'Date: <b>%{{x}}</b><br>'
                    f'Close: <b>$ %{{y:,.2f}}</b>'
                    '<extra></extra>'
                )
            
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
                customdata=customdata,
                hovertemplate=hover_template,
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
            high_90d = self.high_90d_dict.get(symbol, 0)
            low_90d = self.low_90d_dict.get(symbol, 0)
            high_365d = self.high_365d_dict.get(symbol, 0)
            low_365d = self.low_365d_dict.get(symbol, 0)
            
            # Calculate deltas
            delta_90d = high_90d - low_90d
            delta_90d_pct = (delta_90d / low_90d * 100) if low_90d > 0 else 0
            delta_365d = high_365d - low_365d
            delta_365d_pct = (delta_365d / low_365d * 100) if low_365d > 0 else 0
            delta_ath = current - ath
            delta_ath_pct = (delta_ath / ath * 100) if ath > 0 else 0
            
            # ATH bar (hidden from legend)
            fig.add_trace(go.Bar(
                name=f'{symbol} ATH',
                y=[symbol],
                x=[ath],
                legendgroup=symbol,
                marker_color=self._convert_color(color_b, 0.6),
                orientation='h',
                hovertemplate=(
                    f'<b>{symbol} - All-Time-High</b><br><br>'
                    f'ATH Price: <b>$ {ath:,.2f}</b><br>'
                    f'Current Price: <b>$ {current:,.2f}</b><br>'
                    f'Δ from ATH: <b>$ {delta_ath:,.2f} ({delta_ath_pct:+.2f}%)</b><br><br>'
                    f'<i>90-Day Range:</i><br>'
                    f'  High: <b>$ {high_90d:,.2f}</b><br>'
                    f'  Low: <b>$ {low_90d:,.2f}</b><br>'
                    f'  Δ: <b>$ {delta_90d:,.2f} ({delta_90d_pct:.2f}%)</b><br><br>'
                    f'<i>1-Year Range:</i><br>'
                    f'  High: <b>$ {high_365d:,.2f}</b><br>'
                    f'  Low: <b>$ {low_365d:,.2f}</b><br>'
                    f'  Δ: <b>$ {delta_365d:,.2f} ({delta_365d_pct:.2f}%)</b>'
                    '<extra></extra>'
                ),
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
                hovertemplate=(
                    f'<b>{symbol} - Current Price</b><br><br>'
                    f'Current: <b>$ {current:,.2f}</b><br>'
                    f'ATH: <b>$ {ath:,.2f}</b><br>'
                    f'Δ from ATH: <b>$ {delta_ath:,.2f} ({delta_ath_pct:+.2f}%)</b><br><br>'
                    f'<i>90-Day Range:</i><br>'
                    f'  High: <b>$ {high_90d:,.2f}</b><br>'
                    f'  Low: <b>$ {low_90d:,.2f}</b><br>'
                    f'  Δ: <b>$ {delta_90d:,.2f} ({delta_90d_pct:.2f}%)</b><br><br>'
                    f'<i>1-Year Range:</i><br>'
                    f'  High: <b>$ {high_365d:,.2f}</b><br>'
                    f'  Low: <b>$ {low_365d:,.2f}</b><br>'
                    f'  Δ: <b>$ {delta_365d:,.2f} ({delta_365d_pct:.2f}%)</b>'
                    '<extra></extra>'
                ),
                showlegend=False
            ), row=1, col=2)
            
            # Add 90-day high/low span as a line (green)
            fig.add_trace(go.Scatter(
                x=[low_90d, high_90d],
                y=[symbol, symbol],
                mode='lines+markers',
                name=f'{symbol} 90d Range',
                legendgroup=symbol,
                line=dict(color='rgba(26, 188, 156, 0.8)', width=3),
                marker=dict(size=8, symbol='diamond', color='rgba(26, 188, 156, 0.8)'),
                hovertemplate=(
                    f'<b>{symbol} - 90-Day Range</b><br><br>'
                    f'High: <b>$ {high_90d:,.2f}</b><br>'
                    f'Low: <b>$ {low_90d:,.2f}</b><br>'
                    f'Δ: <b>$ {delta_90d:,.2f} ({delta_90d_pct:.2f}%)</b>'
                    '<extra></extra>'
                ),
                showlegend=False
            ), row=1, col=2)
            
            # Add 1-year high/low span as a line (red)
            fig.add_trace(go.Scatter(
                x=[low_365d, high_365d],
                y=[symbol, symbol],
                mode='lines+markers',
                name=f'{symbol} 1yr Range',
                legendgroup=symbol,
                line=dict(color='rgba(231, 76, 60, 0.8)', width=2, dash='dot'),
                marker=dict(size=6, symbol='square', color='rgba(231, 76, 60, 0.8)'),
                hovertemplate=(
                    f'<b>{symbol} - 1-Year Range</b><br><br>'
                    f'High: <b>$ {high_365d:,.2f}</b><br>'
                    f'Low: <b>$ {low_365d:,.2f}</b><br>'
                    f'Δ: <b>$ {delta_365d:,.2f} ({delta_365d_pct:.2f}%)</b>'
                    '<extra></extra>'
                ),
                showlegend=False
            ), row=1, col=2)
        
        # Row 2: Rolling Correlation Plot (Last 90 days)
        # Add background zones using shapes instead of hrect
        if not df_btc.empty:
            # Get last 90 days of data
            cutoff_date = df_btc['Date'].max() - pd.Timedelta(days=90)
            
            # Plot correlation lines for each altcoin (exclude BTC)
            for symbol in self.symbols:
                if symbol == 'BTC' or symbol not in self.correlation_series:
                    continue
                
                corr_series = self.correlation_series[symbol]
                if corr_series.empty:
                    continue
                
                # Merge with dates and filter last 90 days
                df_symbol = self.all_data[symbol]
                
                # Safely align correlation series with df_symbol using reindex
                corr_aligned = corr_series.reindex(df_symbol.index).fillna(0)
                
                df_corr = pd.DataFrame({
                    'Date': df_symbol['Date'],
                    'Correlation': corr_aligned.values
                })
                df_corr = df_corr[df_corr['Date'] >= cutoff_date].dropna()
                
                if df_corr.empty:
                    continue
                
                color_a = self.config.get_crypto_color(symbol, 'primary')
                
                fig.add_trace(go.Scatter(
                    x=df_corr['Date'], # x-axis dates
                    y=df_corr['Correlation'], # y-axis correlation values
                    mode='lines', # line plot
                    name=f'{symbol} Correlation', # legend name
                    legendgroup=symbol, # group by symbol
                    line=dict(color=self._convert_color(color_a, 0.9), width=2),
                    hovertemplate=f'<b>{symbol}</b><br>Date: <b>%{{x}}</b><br>Correlation: <b>%{{y:.3f}}</b><extra></extra>',
                    showlegend=False
                ), row=2, col=1)
        
        # Update layout
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_yaxes(title_text="Price (USD)", type="log", row=1, col=1)
        fig.update_xaxes(title_text="Price (USD)", type="log", row=1, col=2)
        fig.update_yaxes(title_text="", row=1, col=2)
        fig.update_xaxes(title_text="Date", row=2, col=1, title_font=dict(size=14))
        fig.update_yaxes(title_text="Correlation Coefficient", range=[-0.2, 1.05], row=2, col=1, title_font=dict(size=14))
        
        # Calculate cutoff date for shapes
        cutoff_date = df_btc['Date'].max() - pd.Timedelta(days=90) if not df_btc.empty else pd.Timestamp.now()
        date_max = df_btc['Date'].max() if not df_btc.empty else pd.Timestamp.now()
        
        fig.update_layout(
            barmode='overlay',
            template=self.config.get_plotly_template(),
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
                    text="Select/deselect symbol by clicking on it",
                    font=dict(size=14, color="#47356A"),
                    side="top"
                )
            ),
            autosize=True,
            # height=1100,
            margin=dict(l=30, r=30, t=100, b=100),
            shapes=[
                # Green zone - Strong coupling
                dict(
                    type="rect",
                    xref="x3", yref="y3",
                    x0=cutoff_date,
                    x1=date_max,
                    y0=0.7, y1=1.0,
                    fillcolor="green",
                    opacity=0.1,
                    layer="below",
                    line_width=0,
                ),
                # Yellow zone - Moderate correlation
                dict(
                    type="rect",
                    xref="x3", yref="y3",
                    x0=cutoff_date,
                    x1=date_max,
                    y0=0.3, y1=0.7,
                    fillcolor="yellow",
                    opacity=0.1,
                    layer="below",
                    line_width=0,
                ),
                # Red zone - Decoupling
                dict(
                    type="rect",
                    xref="x3", yref="y3",
                    x0=cutoff_date,
                    x1=date_max,
                    y0=-0.2, y1=0.3,
                    fillcolor="red",
                    opacity=0.1,
                    layer="below",
                    line_width=0,
                ),
            ],
        )
        
        # Now add the color zone labels to existing annotations (subplot titles)
        # Get existing annotations (subplot titles) and append zone labels
        current_annotations = list(fig.layout.annotations)
        
        # Style the subplot titles (first 3 annotations) and move them up
        for i in range(min(3, len(current_annotations))):
            current_annotations[i].update(
                font=dict(size=18, color='#47356A', family='Arial, sans-serif'),
                y=current_annotations[i].y + 0.04  # Move titles up
            )
        
        # Add zone label annotations
        zone_labels = [
            dict(
                xref="x3", yref="y3",
                x=cutoff_date,
                y=0.85,
                text="Strong Coupling",
                showarrow=False,
                font=dict(size=14, color="green"),
                xanchor="left"
            ),
            dict(
                xref="x3", yref="y3",
                x=cutoff_date,
                y=0.5,
                text="Moderate",
                showarrow=False,
                font=dict(size=14, color="orange"),
                xanchor="left"
            ),
            dict(
                xref="x3", yref="y3",
                x=cutoff_date,
                y=0.1,
                text="Decoupling",
                showarrow=False,
                font=dict(size=14, color="red"),
                xanchor="left"
            ),
        ]
        
        # Update layout with combined annotations
        fig.update_layout(annotations=current_annotations + zone_labels)
        
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
        
        # Quick summary box
        summary_box = pn.pane.Markdown(
            """
            **Quick Overview:** <br>
            <br>
            This dashboard provides comprehensive market analysis including historical price comparisons, 
            volatility analysis through correlation and beta coefficients, trading ranges (90-day and 1-year), and BTC coupling dynamics. 
            Hover over charts for detailed metrics. <br>
            <br>
            *See bottom of page for detailed explanations.*
            """,
            styles={
                'font-size': '14px',
                'background-color': '#f8f9fa',
                'color': '#2c3e50',
                'padding': '12px 20px',
                'border-radius': '5px',
                'border-left': f'4px solid {self.config.primary_color}',
                'margin': '10px 0px'
            },
            sizing_mode='stretch_width'
        )
        
        # Explanation text for correlation and beta
        explanation_combined = pn.pane.Markdown(
            """
            ## Market Coupling Analysis
            
            This dashboard analyzes how altcoins correlate with Bitcoin over time.
            
            **Chart Descriptions:**
            - **Price Chart (Top Left)**: Hover to see historical 30-day rolling correlation and beta at any point in time
            - **Current Price vs ATH Chart (Top Right)**: Visualizes how close each cryptocurrency is to its all-time high price
             and shows recent 90-day and 1-year trading ranges
            - **Correlation Chart (Bottom)**: Shows recent 90-day correlation trends with color-coded zones:
              - 🟢 **Green (> 0.7)**: Strong coupling - altcoin moves together with BTC
              - 🟡 **Yellow (0.3 - 0.7)**: Moderate correlation
              - 🔴 **Red (< 0.3)**: Decoupling - altcoin moves independently from BTC
            
            ---
            
            **Understanding the Metrics:**
            
            **30d Correlation (Pearson):** Measures price movement similarity with BTC over 30 days
            - **> 0.7**: Strong coupling (moves together with BTC)
            - **0.3 - 0.7**: Moderate correlation
            - **< 0.3**: Decoupling (moves independently from BTC)
            - **Range**: -1 (opposite direction) to +1 (same direction)
            
            **30d Beta Coefficient:** Measures volatility relative to BTC movements
            - **Beta > 1**: More volatile than BTC (amplified movements)
            - **Beta = 1**: Moves in line with BTC
            - **Beta < 1**: Less volatile than BTC
            - **Beta < 0**: Moves opposite to BTC
            
            *Example: A beta of 1.5 means the asset moves 50% more than BTC in the same direction*
            """,
            styles={
                'font-size': '14px',
                'background-color': '#47356A',
                'color': 'white',
                'padding': '20px',
                'border-radius': '5px',
                'margin-top': '10px'
            },
            sizing_mode='stretch_width'
        )
        
        # Create reactive pane for combined plot
        self.plot_pane = pn.Column(sizing_mode='stretch_both', min_height=1200)
        
        # Initialize with current data
        self._update_display()
        
        # Create layout with responsive design - single combined plot
        layout = pn.Column(
            header,
            summary_box,
            pn.layout.Divider(),
            self.plot_pane,
            explanation_combined,
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
