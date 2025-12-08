"""
Base Dashboard Class
Abstract base class for all dashboard implementations.
"""

import panel as pn
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseDashboard(ABC):
    """Abstract base class for dashboard implementations."""
    
    # Class attributes that can be overridden by subclasses
    display_name: str = "Base Dashboard"
    description: str = "Base dashboard class"
    version: str = "2.5"
    author: str = "kuranez"
    
    def __init__(self):
        """Initialize the dashboard."""
        self.widgets = {}
        self.plots = {}
        self.data = {}
    
    @abstractmethod
    def create_dashboard(self) -> pn.Column:
        """
        Create and return the dashboard layout.
        
        Returns:
            pn.Column: The main dashboard layout
        """
        pass
    
    def get_widgets(self) -> Dict[str, Any]:
        """Get all interactive widgets for this dashboard."""
        return self.widgets
    
    def get_plots(self) -> Dict[str, Any]:
        """Get all plots for this dashboard."""
        return self.plots
    
    def refresh_data(self):
        """Refresh/reload data for the dashboard."""
        pass
    
    def export_data(self, format: str = 'csv') -> str:
        """Export dashboard data in specified format."""
        return ""
    
    def get_dependencies(self) -> List[str]:
        """Get list of required packages for this dashboard."""
        return [
            'panel>=1.3.0',
            'plotly>=5.0.0',
            'pandas>=1.3.0'
        ]

    def _create_footer_row(self):
        """Create the footer row with author info and repository links."""
        import base64
        from pathlib import Path
        
        # Lazy import to avoid hard dependency if not used
        try:
            from config import AppConfig
            config = AppConfig()
            primary_color = getattr(config, 'primary_color', '#47356A')
        except Exception:
            primary_color = '#47356A'
        
        github_logo_path = Path(__file__).resolve().parent.parent / 'assets' / 'github_logo.png'
        try:
            with open(github_logo_path, 'rb') as f:
                logo_data = base64.b64encode(f.read()).decode()
        except Exception:
            logo_data = ''
        
        footer_text = f"""
        <div style="text-align: center; background-color: #008080; color: white; padding: 20px; border-radius: 4px;">
        <a href="https://github.com/kuranez/" target="_blank"><img src="data:image/png;base64,{logo_data}" alt="GitHub" width="32"></a><br>
        <b>Created by <a href="https://github.com/kuranez/" style="color: white; text-decoration: none;">kuranez</a> | Version 2.5</b><br>
        <b><a href="https://github.com/kuranez/krypto-dashboard-webapp" style="color: white; text-decoration: none;">🌐 Web Version</a> | 
        <a href="https://github.com/kuranez/krypto-dashboard" style="color: white; text-decoration: none;">📙 Jupyter Notebook Version</a></b>
        <br><br>
        <b>Support the project with a donation:</b><br>
        <hr style="border-color: white;">
        <b>BTC</b> bc1qvh86xt0zr7g2lsqjdez4rk3s5ncpmt7urhugr8 <b>|</b> 
        <b>ETH</b> 0xb4a0a7f883959c33b2b5dfd1722b6098ee9fa447 <b>|</b> 
        <b>BNB</b> 0xb4a0a7f883959c33b2b5dfd1722b6098ee9fa447 <br>
        <b>SOL</b> 9GCKataSxeHPhpKssHiVq1TNW8N32bNwVJJ7hy12EA9T <b>|</b> 
        <b>Polygon</b> 0xb4a0a7f883959c33b2b5dfd1722b6098ee9fa447
        </div>
        """
        return pn.pane.Markdown(footer_text, sizing_mode='stretch_width', styles={'width': '100%'})
