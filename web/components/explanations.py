import panel as pn


def technical_analysis_guide() -> pn.pane.Markdown:
    text = """
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
    """
    return pn.pane.Markdown(
        text,
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


def market_coupling_explanation() -> pn.pane.Markdown:
    text = """
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
    """
    return pn.pane.Markdown(
        text,
        styles={
            'font-size': '16px',
            'background-color': '#47356A',
            'color': 'white',
            'padding': '20px',
            'border-radius': '5px',
            'margin-top': '10px'
        },
        sizing_mode='stretch_width'
    )
