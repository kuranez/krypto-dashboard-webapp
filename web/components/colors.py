"""
Color utilities for consistent RGBA conversion across charts.
"""
import matplotlib.colors as mcolors

def to_rgba(color_name, opacity=1.0):
    """Convert color name to rgba string."""
    rgba = mcolors.to_rgba(color_name, opacity)
    return f'rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {rgba[3]})'
