"""
PrettyPlots: Publication-ready plotting with a clean, modular API.

PrettyPlots provides a seaborn-like interface for creating beautiful,
publication-ready visualizations with sensible defaults and extensive
customization options.

Basic usage:
    >>> import prettyplots as pp
    >>> pp.set_publication_style()
    >>> fig, ax = pp.barplot(data=df, x='category', y='value')
    >>> pp.savefig(fig, 'output.png')
"""

__version__ = "0.1.0"
__author__ = "Jorge Botas"

# Core plotting functions (base)
from prettyplots.base.bar import barplot
from prettyplots.base.scatter import scatterplot
from prettyplots.base.heatmap import circle_heatmap

# Advanced plotting functions
from prettyplots.advanced.venn import venn

# Utilities
from prettyplots.utils.io import savefig, save_multiple, close_all
from prettyplots.utils.axes import (
    adjust_spines,
    add_grid,
    set_axis_labels,
    add_reference_line,
)
from prettyplots.utils.legend import (
    HandlerCircle,
    HandlerRectangle,
    get_legend_handler_map,
    create_legend_handles,
    LegendBuilder,
    create_legend_builder,
)

# Theming
from prettyplots.themes.colors import get_palette, list_palettes, show_palette, resolve_palette, DEFAULT_COLOR
from prettyplots.themes.styles import (
    set_publication_style,
    set_minimal_style,
    set_poster_style,
    reset_style,
)
from prettyplots.themes.markers import (
    get_marker_cycle,
    get_hatch_cycle,
    STANDARD_MARKERS,
    HATCH_PATTERNS,
)
from prettyplots.themes.hatches import (
    set_hatch_mode,
    get_hatch_mode,
    get_hatch_patterns,
    list_hatch_patterns,
)

__all__ = [
    "__version__",
    "__author__",
    # Base plots
    "barplot",
    "scatterplot",
    "circle_heatmap",
    # Advanced plots
    "venn",
    # I/O utilities
    "savefig",
    "save_multiple",
    "close_all",
    # Axes utilities
    "adjust_spines",
    "add_grid",
    "set_axis_labels",
    "add_reference_line",
    # Legend utilities
    "HandlerCircle",
    "HandlerRectangle",
    "get_legend_handler_map",
    "create_legend_handles",
    "LegendBuilder",
    "create_legend_builder",
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
    # Hatch functions
    "set_hatch_mode",
    "get_hatch_mode",
    "get_hatch_patterns",
    "list_hatch_patterns",
    # Constants
    "STANDARD_MARKERS",
    "HATCH_PATTERNS",
]
