"""
Configuration and Styling
Application-wide configuration and styling constants.
"""

class AppConfig:
    """Application configuration and styling."""
    
    def __init__(self):
        
        # Supported cryptocurrency symbols
        self.available_symbols = [
            'BTC', 'ETH', 'BNB', 'TRX', 'SOL',
            'ADA', 'DOT', 'UNI', 'XRP', 'XLM',
            'LINK', 'LTC', 'DOGE', 'SHIB', 'HBAR'
        ]

        # Color scheme for the application
        self.accent_color = "teal"

        self.primary_color = "#47356A"  # Main purple
        self.secondary_color = "#20B2AA"  # Teal
        self.tertiary_color = "#008080"  # Dark teal

        self.primary_text_color = "#47356A"
        self.secondary_text_color = "#2c3e50"

        self.red_color = "#e74c3c"  # Used for negative/alert
        self.green_color = "#1abc9c"  # Used for positive/success
        self.orange_color = "#f39c12"  # Used for warning/highlight
        self.blue_color = "#3498db"  # Used for info/volume
        self.gold_color = "#ffd700"  # Used for gold/secondary
        self.gray_color = "#808080"  # Used for grid/neutral
        self.light_gray_color = "#f8f9fa"  # Used for backgrounds
        self.background_color = "#ffebee"  # Used for error/info backgrounds
        self.white_color = "#ffffff"
        self.black_color = "#000000"

        
        # Component styling
        self.styles = {
            "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
            "border-radius": "4px",
            "padding": "10px",
            "font-size": "18px",
        }
        
        
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
