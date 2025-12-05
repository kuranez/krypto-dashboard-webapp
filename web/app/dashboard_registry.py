"""
Dashboard Registry
Manages discovery and loading of dashboard modules.
"""

import importlib.util
import inspect
from pathlib import Path
from typing import Dict, Type
from base_dashboard import BaseDashboard

class DashboardRegistry:
    """Registry for discovering and managing dashboard modules."""
    
    def __init__(self):
        self.dashboards: Dict[str, Type[BaseDashboard]] = {}
        self.dashboard_paths = [
            Path(__file__).parent.parent / "dashboards",
            Path(__file__).parent.parent / "example_dashboards" / "simple"
        ]
    
    def discover_dashboards(self):
        """Discover all available dashboard modules."""
        self.dashboards.clear()
        
        for dashboard_dir in self.dashboard_paths:
            if dashboard_dir.exists():
                self._scan_directory(dashboard_dir)
    
    def _scan_directory(self, directory: Path):
        """Scan a directory for dashboard Python files."""
        for file_path in directory.glob("*.py"):
            if file_path.name.startswith('_'):
                continue
                
            try:
                self._load_dashboard_module(file_path)
            except Exception as e:
                print(f"Error loading dashboard from {file_path}: {e}")
    
    def _load_dashboard_module(self, file_path: Path):
        """Load a dashboard module and extract dashboard classes."""
        module_name = file_path.stem
        
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load spec for {file_path}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for dashboard classes or create wrapper
        dashboard_class = None
        
        # First, look for classes that inherit from BaseDashboard
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseDashboard) and obj != BaseDashboard:
                dashboard_class = obj
                break
        
        # If no BaseDashboard subclass found, create a wrapper
        if not dashboard_class:
            dashboard_class = self._create_dashboard_wrapper(module, module_name)
        
        if dashboard_class:
            # Use the class name or module name as the dashboard name
            dashboard_name = getattr(dashboard_class, 'display_name', module_name.replace('_', ' ').title())
            self.dashboards[dashboard_name] = dashboard_class
    
    def _create_dashboard_wrapper(self, module, module_name):
        """Create a wrapper class for legacy dashboard modules."""
        
        class DynamicDashboard(BaseDashboard):
            display_name = module_name.replace('_', ' ').title()
            description = f"Dashboard from {module_name}.py"
            version = "1.1"
            author = "Auto-generated & modified by kuranez"
            
            def __init__(self):
                super().__init__()
                self.module = module
                
                # Try to find key functions in the module
                self.plot_functions = []
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    if name.startswith('plot_') or 'plot' in name.lower():
                        self.plot_functions.append((name, obj))
            
            def create_dashboard(self):
                """Create dashboard from module functions."""
                import panel as pn
                
                components = []
                components.append(pn.pane.Markdown(f"## {self.display_name}"))
                
                # If the module has a main function, try to extract plots from it
                if hasattr(self.module, 'main'):
                    try:
                        self.module.main()
                    except Exception as e:
                        components.append(pn.pane.Markdown(f"Error executing main: {e}"))
                
                # Execute and capture plotting functions
                for func_name, func in self.plot_functions:
                    try:
                        result = func()
                        if result is not None:
                            components.append(result)
                    except Exception as e:
                        components.append(pn.pane.Markdown(f"Error in {func_name}: {e}"))
                
                # Show available functions
                if self.plot_functions:
                    func_list = "\\n".join([f"- {name}" for name, _ in self.plot_functions])
                    components.append(pn.pane.Markdown(f"**Available plotting functions:**\\n{func_list}"))
                
                return pn.Column(*components)
        
        return DynamicDashboard
    
    def get_dashboard(self, name: str) -> Type[BaseDashboard]:
        """Get a dashboard class by name."""
        return self.dashboards.get(name)
    
    def get_available_dashboards(self) -> Dict[str, Type[BaseDashboard]]:
        """Get all available dashboards."""
        return self.dashboards.copy()
    
    def register_dashboard(self, name: str, dashboard_class: Type[BaseDashboard]):
        """Manually register a dashboard class."""
        self.dashboards[name] = dashboard_class
