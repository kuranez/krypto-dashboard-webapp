"""
Cryptocurrency Dashboard App

A modular dashboard application built with HoloViz Panel for cryptocurrency data visualization.
"""

__version__ = "2.0.0"
__author__ = "Dashboard Team"
__description__ = "Modular cryptocurrency dashboard with Panel"

# Import main components for easy access
from .main import create_app, DashboardApp
from .base_dashboard import BaseDashboard
from .data_manager import DataManager
from .figure_factory import FigureFactory
from .config import AppConfig

__all__ = [
    'create_app',
    'DashboardApp', 
    'BaseDashboard',
    'DataManager',
    'FigureFactory',
    'AppConfig'
]
