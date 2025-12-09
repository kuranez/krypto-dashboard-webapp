"""
Main Dashboard Application
HoloViz Panel-based cryptocurrency dashboard with modular dashboard support.
"""

from pathlib import Path
import sys

import panel as pn
import param

from config import AppConfig
from dashboard_registry import DashboardRegistry

# Ensure app directory is on sys.path so 'components' and other subpackages import reliably
_app_dir = Path(__file__).parent
for p in (str(_app_dir), str(_app_dir.parent)):
    if p not in sys.path:
        sys.path.append(p)

pn.extension('plotly')

class DashboardApp(param.Parameterized):
    """Main dashboard application class."""
    
    selected_dashboard = param.Parameter(default=None)
    
    def __init__(self, **params):
        super().__init__(**params)
        self.config = AppConfig()
        self.registry = DashboardRegistry()
        self.current_dashboard_instance = None
        self.registry.discover_dashboards()
        # Create UI components
        self._create_main_area()
        self._create_header()
        # Load initial dashboard
        dashboard_names = list(self.registry.get_available_dashboards().keys())
        if dashboard_names:
            self._load_dashboard(dashboard_names[0])
        
    def _create_header(self):
        """Create the header with logo and dashboard selector."""
        dashboard_names = list(self.registry.get_available_dashboards().keys())
        
        # Title
        title_pane = pn.pane.Markdown(
            "### Select a Dashboard",
            styles={'color': 'white', 'margin': '0px'},
            margin=(10, 20)
        )
        
        # Dashboard selector with white text
        self.dashboard_selector = pn.widgets.Select(
            name='',
            options=dashboard_names,
            value=dashboard_names[0] if dashboard_names else None,
            width=300,
            margin=(5, 10),
            styles={'color': '#47356A'}
        )
        
        # Load Data button
        self.load_data_button = pn.widgets.Button(
            name='Load Data',
            button_type='primary',
            width=120,
            margin=(5, 10),
            styles={'color': 'white'}
        )
        
        self.dashboard_selector.param.watch(self._on_dashboard_change, 'value')
        self.load_data_button.on_click(self._on_load_data_click)
        
        # Create header row without logo (logo is in template)
        self.header_row = pn.Row(
            title_pane,
            pn.Spacer(),
            self.dashboard_selector,
            self.load_data_button,
            sizing_mode='stretch_width',
            styles={'background': self.config.primary_color, 'padding': '20px', 'border-radius': '4px'},
            height=70
        )
    
    def _create_main_area(self):
        """Create the main content area."""
        # Use a Column so we can update it reactively
        self.main_content = pn.Column(
            pn.pane.Markdown(
                "## Welcome to Crypto Dashboard\nSelect a dashboard from the menu above.",
                margin=(20, 20),
            ),
            sizing_mode='stretch_both'
        )
    
    def _on_dashboard_change(self, event):
        """Handle dashboard selection change."""
        if event.new:
            self._load_dashboard(event.new)
    
    def _on_load_data_click(self, event):
        """Handle load data button click."""
        if self.current_dashboard_instance and hasattr(self.current_dashboard_instance, 'refresh_data'):
            self.current_dashboard_instance.refresh_data()
    
    def _load_dashboard(self, dashboard_name):
        """Load and display the selected dashboard."""
        try:
            dashboard_class = self.registry.get_dashboard(dashboard_name)
            if dashboard_class:
                # Create new dashboard instance
                self.current_dashboard_instance = dashboard_class()
                
                # Update main content with error handling
                try:
                    dashboard_content = self.current_dashboard_instance.create_dashboard()
                    # Clear and update the Column
                    self.main_content.clear()
                    self.main_content.append(dashboard_content)
                except Exception as e:
                    error_pane = pn.pane.Markdown(
                        f"## Error Creating Dashboard\n\n```\n{str(e)}\n```\n\n"
                        f"Please check the dashboard implementation.",
                        styles={'background-color': '#ffebee', 'padding': '20px', 'border-radius': '4px'}
                    )
                    self.main_content.clear()
                    self.main_content.append(error_pane)
                
        except Exception as e:
            error_pane = pn.pane.Markdown(
                f"## Error Loading Dashboard\n\n```\n{str(e)}\n```",
                styles={'background-color': '#ffebee', 'padding': '20px', 'border-radius': '4px'}
            )
            self.main_content.clear()
            self.main_content.append(error_pane)
    
    def create_template(self):
        """Create and return the Panel application."""
        # Use FastListTemplate for proper title display
        template = pn.template.FastListTemplate(
            title="Cryptocurrency Dashboard",
            logo=str(Path(__file__).resolve().parent.parent / 'assets' / 'logo.png'),
            main=[self.header_row, self.main_content],
            main_layout=None,
            accent=self.config.accent_color,
            header_background=self.config.accent_color,
            theme_toggle=False
        )
        
        return template

def create_app():
    """Factory function to create the dashboard app."""
    app = DashboardApp()
    return app.create_template()

# Make the app servable for panel serve command
app = create_app()
app.servable()

if __name__ == "__main__":
    # For development, show the app
    app.show(port=5007)
