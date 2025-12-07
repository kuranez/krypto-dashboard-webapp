"""
Pytest configuration for testing directory.
"""
import sys
from pathlib import Path

# Add the app directory to Python path
project_root = Path(__file__).parent.parent
app_dir = project_root / 'web' / 'app'
sys.path.insert(0, str(app_dir))
