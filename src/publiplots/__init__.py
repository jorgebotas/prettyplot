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

__version__ = "0.2.0"
__author__ = "Jorge Botas"
__license__ = "MIT"
__copyright__ = "Copyright 2025, Jorge Botas"
__url__ = "https://github.com/jorgebotas/publiplots"
__email__ = "jorgebotas.github@gmail.com"
__description__ = "Publication-ready plotting with a clean, modular API"

# Core plotting functions (base)
from publiplots.base.bar import barplot
from publiplots.base.scatter import scatterplot

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
    HandlerCircle,
    HandlerRectangle,
    get_legend_handler_map,
    create_legend_handles,
    LegendBuilder,
    create_legend_builder,
)

# Theming
from publiplots.themes.colors import get_palette, list_palettes, show_palette, resolve_palette
from publiplots.themes.styles import (
    set_notebook_style,
    set_publication_style,
    set_illustrator_style,  # Backward compatibility alias
    set_minimal_style,
    set_poster_style,
    reset_style,
)
# Initialize publiplots rcParams defaults
from publiplots.themes.defaults import init_rcparams
init_rcparams()
from publiplots.themes.markers import (
    get_marker_cycle,
    get_hatch_cycle,
    STANDARD_MARKERS,
    HATCH_PATTERNS,
)
from publiplots.themes.hatches import (
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
    # Style functions
    "set_notebook_style",
    "set_publication_style",
    "set_illustrator_style",  # Backward compatibility alias
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
