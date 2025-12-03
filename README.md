# Cryptocurrency Dashboard

<p align="left">
    <a href="https://www.python.org/" target="_blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
    </a>
    <a href="https://panel.holoviz.org/" target="_blank">
        <img src="https://img.shields.io/badge/Holoviz%20Panel-0094A9?style=for-the-badge" alt="Holoviz Panel"/>
    </a>
    <a href="https://docs.docker.com/" target="_blank">
        <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
    </a>
</p>


A modular, extensible cryptocurrency dashboard built with HoloViz Panel. Based on previous project: https://github.com/kuranez/krypto-dashboard

## 🌐 Web App

> [![Live Demo](https://img.shields.io/badge/🟢%20Live%20App-%20Krypto--Dashboard--0057B7?style=for-the-badge)](https://apps.kuracodez.space/krypto-dashboard/main)
>
> **Try the app - explore cryptocurrency prices directly in your browser.**

## Screenshot

> ![https://raw.githubusercontent.com/kuranez/krypto-dashboard-webapp/refs/heads/main/screenshots/Screenshot_market_overview.png](https://raw.githubusercontent.com/kuranez/krypto-dashboard-webapp/refs/heads/main/screenshots/Screenshot_market_overview.png)

## Features

- 🔄 **Modular Architecture**: Easy to add new dashboards
- 📊 **Interactive Visualizations**: Built with Plotly and Panel
- 🎨 **Consistent Styling**: Centralized theming and configuration
- 💾 **Data Caching**: Efficient API usage with Panel caching
- 🔌 **Plugin System**: Auto-discovery of dashboard modules

## Quick Start

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r web/requirements.txt
   ```

2. **Launch the App**:
   ```bash
   python web/app/launch.py
   ```

3. **Open Browser**: Navigate to http://localhost:5007

### Docker (Production)

1. **Pull from GitHub Container Registry**:
   ```bash
   docker pull ghcr.io/kuranez/krypto-dashboard-web:latest
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Access**: http://localhost:5013/krypto-dashboard

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
web/
├── app/
│   ├── main.py                    # Main application
│   ├── launch.py                  # Local development launcher
│   ├── dashboard_registry.py      # Dashboard discovery
│   ├── base_dashboard.py         # Base dashboard class
│   ├── data_manager.py           # Data management
│   ├── figure_factory.py         # Chart creation
│   ├── config.py                 # Configuration
│   └── requirements.txt          # Dependencies
├── dashboards/
│   ├── simple_price_dashboard.py # Basic price chart
│   ├── detailed_price_chart.py   # Detailed analysis
│   └── market_overview.py        # Market overview
└── assets/
    └── logo.png                   # Application logo
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

### Plesk Server (Production)

1. **Configure Nginx Reverse Proxy** in Plesk:
   ```nginx
   location /krypto-dashboard/ {
       proxy_pass http://localhost:5013/krypto-dashboard/;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection "upgrade";
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   ```

2. **Deploy Container**:
   ```bash
   # Pull latest code
   git pull origin main
   
   # Pull latest image
   docker-compose pull
   
   # Start/restart container
   docker-compose down && docker-compose up -d
   ```

3. **Access**: https://apps.kuracodez.space/krypto-dashboard

### Docker Build & Push

**Build locally:**
```bash
docker-compose -f docker-compose.build.yml build
```

**Push to GitHub Container Registry:**
```bash
docker push ghcr.io/kuranez/krypto-dashboard-web:latest
```

### Environment Variables

Optional API key configuration:
```bash
export BINANCE_API_KEY=your_api_key_here
```

Or set in Plesk Docker stack environment settings.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure dependencies installed: `pip install -r web/requirements.txt`
2. **Port Conflicts**: Local dev uses port 5007, Docker uses 5013
3. **404 Errors on Server**: Verify nginx reverse proxy configuration
4. **WebSocket Errors**: Check `Upgrade` and `Connection` headers in proxy config

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your dashboard to the `dashboards/` directory
4. Test your dashboard
5. Submit a pull request

## License

This project is open source and available under the MIT License. You may modify, distribute, and use it freely in your own projects.
