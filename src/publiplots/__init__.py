"""
PubliPlots: Publication-ready plotting with a clean, modular API.

PubliPlots provides a seaborn-like interface for creating beautiful,
publication-ready visualizations with sensible defaults and extensive
customization options.

Basic usage:
    >>> import publiplots as pp
    >>> pp.set_notebook_style()  # For interactive work
    >>> fig, ax = pp.barplot(data=df, x='category', y='value')
    >>> pp.savefig(fig, 'output.png')
"""

__version__ = "0.4.0"
__author__ = "Jorge Botas"
__license__ = "MIT"
__copyright__ = "Copyright 2025, Jorge Botas"
__url__ = "https://github.com/jorgebotas/publiplots"
__email__ = "jorgebotas.github@gmail.com"
__description__ = "Publication-ready plotting with a clean, modular API"

# Core plotting functions (base)
from publiplots.base.bar import barplot
from publiplots.base.scatter import scatterplot
from publiplots.base.box import boxplot
from publiplots.base.swarm import swarmplot

# Advanced plotting functions
from publiplots.advanced.venn import venn
from publiplots.advanced.upset import upsetplot

# Utilities
from publiplots.utils.io import savefig, save_multiple, close_all
from publiplots.utils.axes import (
    adjust_spines,
    add_grid,
    set_axis_labels,
    add_reference_line,
)
from publiplots.utils.legend import (
    HandlerRectangle,
    HandlerMarker,
    RectanglePatch,
    MarkerPatch,
    get_legend_handler_map,
    create_legend_handles,
    LegendBuilder,
    legend,
)
# Register custom fonts
from publiplots.utils.fonts import _register_fonts
_register_fonts()

# Theming
from publiplots.themes.colors import color_palette
from publiplots.themes.rcparams import rcParams, resolve_param, init_rcparams
from publiplots.themes.styles import (
    set_notebook_style,
    set_publication_style,
    reset_style,
)
# Initialize publiplots rcParams defaults
init_rcparams()
from publiplots.themes.markers import (
    resolve_markers,
    resolve_marker_map,
    STANDARD_MARKERS,
)
from publiplots.themes.hatches import (
    set_hatch_mode,
    get_hatch_mode,
    get_hatch_patterns,
    list_hatch_patterns,
    resolve_hatches,
    resolve_hatch_map,
    HATCH_PATTERNS,
)

__all__ = [
    "__version__",
    "__author__",
    # Base plots
    "barplot",
    "scatterplot",
    "boxplot",
    "swarmplot",
    # Advanced plots
    "venn",
    "upsetplot",
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
    "HandlerRectangle",
    "HandlerMarker",
    "RectanglePatch",
    "MarkerPatch",
    "get_legend_handler_map",
    "create_legend_handles",
    "LegendBuilder",
    "legend",
    # Color/palette functions
    "color_palette",
    # Parameter system
    "rcParams",
    "resolve_param",
    # Style functions
    "set_notebook_style",
    "set_publication_style",
    "reset_style",
    # Marker functions
    "resolve_markers",
    "resolve_marker_map",
    # Hatch functions
    "set_hatch_mode",
    "get_hatch_mode",
    "get_hatch_patterns",
    "list_hatch_patterns",
    "resolve_hatches",
    "resolve_hatch_map",
    # Constants
    "STANDARD_MARKERS",
    "HATCH_PATTERNS",
]
