"""
Configuration and Styling
Application-wide configuration and styling constants.
"""

class AppConfig:
    """Application configuration and styling."""
    
    def __init__(self):
        
        # Color scheme
        self.accent_color = "teal"
        self.primary_color = "#47356A"
        self.secondary_color = "#20B2AA"
        
        # Component styling
        self.styles = {
            "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
            "border-radius": "4px",
            "padding": "10px",
        }
        
        # Layout settings
        # self.sidebar_width = 280
        # self.plot_height = 500
        
        # Cryptocurrency colors for consistency
        self.crypto_colors = {
            'BTC': {
                'primary': 'orange',
                'secondary': 'gold'
            },
            'ETH': {
                'primary': 'mediumpurple',
                'secondary': 'plum'
            },
            'BNB': {
                'primary': 'indianred',
                'secondary': 'lightsalmon'
            },
            'ADA': {
                'primary': 'royalblue',
                'secondary': 'lightblue'
            },
            'DOT': {
                'primary': 'hotpink',
                'secondary': 'pink'
            },
            'DOGE': {
                'primary': 'gold',
                'secondary': 'goldenrod'
            },
            'LTC': {
                'primary': 'silver',
                'secondary': 'gray'
            },
            'XRP': {
                'primary': 'forestgreen',
                'secondary': 'darkgreen'
            },
            'SOL': {
                'primary': 'lightseagreen',
                'secondary': 'mediumpurple'
            },
            'LINK': {
                'primary': 'lightskyblue',
                'secondary': 'dodgerblue'
            },
            'TRX': {
                'primary': 'crimson',
                'secondary': 'tomato'
            },
            'UNI': {
                'primary': 'palevioletred',
                'secondary': 'mediumvioletred'
            },
            'XLM': {
                'primary': 'steelblue',
                'secondary': 'darkblue'
            },
            'SHIB': {
                'primary': 'sandybrown',
                'secondary': 'peru'
            },
            'HBAR': {
                'primary': 'darkslategrey',
                'secondary': 'black'
            }
        }
        
        # Default time intervals
        self.time_intervals = {
            'All_Time': {'days': 'max', 'interval': 'daily'},
            '5Y': {'days': 5*365, 'interval': 'daily'},
            '3Y': {'days': 3*365, 'interval': 'daily'},
            '2Y': {'days': 2*365, 'interval': 'daily'},
            '1Y': {'days': 365, 'interval': 'hourly'},
            '6M': {'days': 180, 'interval': 'hourly'},
            '3M': {'days': 90, 'interval': 'hourly'},
            '1M': {'days': 30, 'interval': 'hourly'},
            '2W': {'days': 14, 'interval': 'hourly'},
            '1W': {'days': 7, 'interval': 'hourly'},
        }
        
        # API settings
        self.api_config = {
            'cache_timeout': 300,  # 5 minutes
            'max_retries': 3,
            'timeout': 30
        }
    
    def get_crypto_color(self, symbol: str, color_type: str = 'primary') -> str:
        """Get color for a cryptocurrency symbol."""
        return self.crypto_colors.get(symbol, {}).get(color_type, 'gray')
    
    def get_plotly_template(self) -> str:
        """Get the default Plotly template."""
        return 'plotly_white'
