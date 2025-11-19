"""
Theming system for publiplots.

This module provides color palettes, styles, and marker definitions
for creating consistent, publication-ready visualizations.
"""

from publiplots.themes.colors import (
    color_palette,
    PALETTES,
)

from publiplots.themes.rcparams import (
    rcParams,
    resolve_param,
)

from publiplots.themes.styles import (
    set_notebook_style,
    set_publication_style,
    reset_style,
    get_current_style,
    apply_custom_style,
)

from publiplots.themes.markers import (
    get_marker_cycle,
    get_hatch_cycle,
    get_size_mapping,
    resolve_markers,
    resolve_marker_mapping,
    STANDARD_MARKERS,
    SIMPLE_MARKERS,
    FILLED_UNFILLED_MARKERS,
    MARKER_SIZES,
    SIZE_RANGE_CATEGORICAL,
    SIZE_RANGE_CONTINUOUS,
)

from publiplots.themes.hatches import (
    get_hatch_patterns,
    set_hatch_mode,
    get_hatch_mode,
    list_hatch_patterns,
    resolve_hatches,
    resolve_hatch_mapping,
    HATCH_PATTERNS,
)

__all__ = [
    # Parameter system
    "rcParams",
    "resolve_param",
    # Color functions
    "color_palette",
    # Color palettes
    "PALETTES",
    # Style functions
    "set_notebook_style",
    "set_publication_style",
    "reset_style",
    "get_current_style",
    "apply_custom_style",
    # Marker functions
    "get_marker_cycle",
    "get_hatch_cycle",
    "get_size_mapping",
    "resolve_markers",
    "resolve_marker_mapping",
    # Marker constants
    "STANDARD_MARKERS",
    "SIMPLE_MARKERS",
    "FILLED_UNFILLED_MARKERS",
    "MARKER_SIZES",
    "SIZE_RANGE_CATEGORICAL",
    "SIZE_RANGE_CONTINUOUS",
    # Hatch functions
    "get_hatch_patterns",
    "set_hatch_mode",
    "get_hatch_mode",
    "list_hatch_patterns",
    "resolve_hatches",
    "resolve_hatch_mapping",
    # Hatch constants
    "HATCH_PATTERNS",
]
