"""
PrettyPlot: Publication-ready plotting with a clean, modular API.

PrettyPlot provides a seaborn-like interface for creating beautiful,
publication-ready visualizations with sensible defaults and extensive
customization options.

Basic usage:
    >>> import prettyplot as pp
    >>> pp.set_publication_style()
    >>> fig, ax = pp.barplot(data=df, x='category', y='value')
    >>> pp.savefig(fig, 'output.png')
"""

__version__ = "0.1.0"
__author__ = "Jorge Botas"

# Core plotting functions (base)
from prettyplot.base.bar import barplot
from prettyplot.base.heatmap import circle_heatmap

# Advanced plotting functions
from prettyplot.advanced.venn import venn_diagram

# Utilities
from prettyplot.utils.io import savefig, save_multiple, close_all
from prettyplot.utils.axes import (
    adjust_spines,
    add_grid,
    set_axis_labels,
    add_reference_line,
)

# Theming
from prettyplot.themes.colors import get_palette, list_palettes, show_palette, resolve_palette, DEFAULT_COLOR
from prettyplot.themes.styles import (
    set_publication_style,
    set_minimal_style,
    set_poster_style,
    reset_style,
)
from prettyplot.themes.markers import (
    get_marker_cycle,
    get_hatch_cycle,
    STANDARD_MARKERS,
    HATCH_PATTERNS,
)

__all__ = [
    "__version__",
    "__author__",
    # Base plots
    "barplot",
    "circle_heatmap",
    # Advanced plots
    "venn_diagram",
    # I/O utilities
    "savefig",
    "save_multiple",
    "close_all",
    # Axes utilities
    "adjust_spines",
    "add_grid",
    "set_axis_labels",
    "add_reference_line",
    # Color/palette functions
    "get_palette",
    "list_palettes",
    "show_palette",
    "resolve_palette",
    # Color constants
    "DEFAULT_COLOR",
    # Style functions
    "set_publication_style",
    "set_minimal_style",
    "set_poster_style",
    "reset_style",
    # Marker functions
    "get_marker_cycle",
    "get_hatch_cycle",
    # Constants
    "STANDARD_MARKERS",
    "HATCH_PATTERNS",
]
