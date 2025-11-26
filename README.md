# Cryptocurrency Dashboard

A modular, extensible cryptocurrency dashboard built with HoloViz Panel.

## Features

- 🔄 **Modular Architecture**: Easy to add new dashboards
- 📊 **Interactive Visualizations**: Built with Plotly and Panel
- 🎨 **Consistent Styling**: Centralized theming and configuration
- 💾 **Data Caching**: Efficient API usage with Panel caching
- 🔌 **Plugin System**: Auto-discovery of dashboard modules

## Quick Start

### Using Docker (Recommended)

1. **Pull and run from GitHub Container Registry**:
   ```bash
   docker run -p 5013:5013 ghcr.io/kuranez/krypto-dashboard-web:latest
   ```

2. **Or use Docker Compose**:
   ```bash
   docker-compose up
   ```

3. **With API key** (optional):
   ```bash
   docker run -p 5013:5013 -e BINANCE_API_KEY=your_key ghcr.io/kuranez/krypto-dashboard-web:latest
   ```

4. **Open Browser**: Navigate to http://localhost:5007

### Local Installation

1. **Install Dependencies**:
   ```bash
   pip install -r app/requirements.txt
   ```

2. **Set up API Key** (optional):
   Create a `keys.env` file in the project root:
   ```
   BINANCE_API_KEY=your_api_key_here
   ```

3. **Launch the App**:
   ```bash
   python launch.py
   ```

4. **Open Browser**: Navigate to http://localhost:5007

## Architecture

### Core Components

- **`main.py`**: Application entry point and layout management
- **`dashboard_registry.py`**: Auto-discovery and loading of dashboard modules
- **`base_dashboard.py`**: Abstract base class for all dashboards
- **`data_manager.py`**: Centralized data fetching and caching
- **`figure_factory.py`**: Standardized chart creation utilities
- **`config.py`**: Application-wide configuration and styling

### Dashboard Structure

```
app/
├── main.py                 # Main application
├── dashboard_registry.py   # Dashboard discovery
├── base_dashboard.py      # Base dashboard class
├── data_manager.py        # Data management
├── figure_factory.py      # Chart creation
├── config.py             # Configuration
├── launch.py             # Launch script
└── requirements.txt      # Dependencies

dashboards/
├── simple_price_dashboard.py  # Basic price and volume chart
├── detailed_price_chart.py  # Detailed price and volume chart
├── market_overview.py  # Market overview for major chains
└── [your_dashboard].py         # Add your dashboards here

krypto-dashboard/
├── launch_simple.py                # ✅ Quick launcher for testing
├── example_usage.py                # ✅ Example of modular usage
└── test_simple.py                  # ✅ Working test script
```

## Creating New Dashboards

### Method 1: Inherit from BaseDashboard

```python
from base_dashboard import BaseDashboard
import panel as pn

class MyDashboard(BaseDashboard):
    display_name = "My Custom Dashboard"
    description = "Description of what this dashboard does"
    version = "1.0"
    author = "Your Name"
    
    def create_dashboard(self) -> pn.Column:
        # Create your dashboard layout here
        return pn.Column(
            pn.pane.Markdown("## My Dashboard"),
            # Add your components
        )
```

### Method 2: Legacy Python Files

Simply place any Python file with plotting functions in the `dashboards/` directory. The registry will automatically wrap it and make it available in the app.

## Configuration

Edit `config.py` to customize:

- **Colors**: Cryptocurrency-specific color schemes
- **Styling**: Component styles and layout settings
- **API Settings**: Timeouts, retries, cache duration
- **Time Intervals**: Available time period options

## Data Sources

- **Binance US API**: Real-time and historical cryptocurrency data
- **Local CSV**: Fallback data sources
- **Caching**: Automatic caching reduces API calls

## Deployment

### Docker (Recommended)

**Pull from GitHub Container Registry:**
```bash
docker pull ghcr.io/kuranez/krypto-dashboard-web:latest
docker run -p 5013:5013 ghcr.io/kuranez/krypto-dashboard-web:latest
```

**Build locally:**
```bash
docker build -t krypto-dashboard-web .
docker run -p 5013:5013 krypto-dashboard-web
```

**Using Docker Compose:**
```bash
docker-compose up -d
```

**Building and pushing to ghcr.io:**
```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and tag
docker build -t ghcr.io/kuranez/krypto-dashboard-web:latest .

# Push to registry
docker push ghcr.io/kuranez/krypto-dashboard-web:latest
```

### Local Development
```bash
python launch.py
```

### Production with Panel Serve
```bash
panel serve app/main.py --port 5007 --allow-websocket-origin=*
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
2. **API Errors**: Check your `keys.env` file and API key
3. **Port Conflicts**: Change the port in `launch.py` if 5007 is in use
4. **Data Loading**: Check your internet connection for API access

### Development Tips

- Use `autoreload=True` in development for hot reloading
- Check browser console for JavaScript errors
- Use Panel's debugging features: `pn.config.console_output = 'accumulate'`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your dashboard to the `dashboards/` directory
4. Test your dashboard
5. Submit a pull request

## License

This project is open source and available under the MIT License. You may modify, distribute, and use it freely in your own projects.
