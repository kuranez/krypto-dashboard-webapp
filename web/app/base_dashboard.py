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
    version: str = "2.0"
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
