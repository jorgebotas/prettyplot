"""
Theming system for publiplots.

This module provides color palettes, styles, and marker definitions
for creating consistent, publication-ready visualizations.
"""

from publiplots.themes.colors import (
    get_palette,
    list_palettes,
    show_palette,
    resolve_palette,
    PASTEL_CATEGORICAL,
    PASTEL_CATEGORICAL_MINIMAL,
    PASTEL_SEQUENTIAL_GREEN,
    PASTEL_SEQUENTIAL_BLUE,
    PASTEL_SEQUENTIAL_PURPLE,
    PASTEL_DIVERGING_RED_BLUE,
    PASTEL_DIVERGING_GREEN_PURPLE,
    PASTEL_SIGNIFICANCE,
    PASTEL_POSITIVE_NEGATIVE,
)

from publiplots.themes.styles import (
    set_notebook_style,
    set_publication_style,
    set_illustrator_style,  # Backward compatibility alias
    set_minimal_style,
    set_poster_style,
    reset_style,
    get_current_style,
    apply_custom_style,
)

from publiplots.themes.markers import (
    get_marker_cycle,
    get_hatch_cycle,
    get_size_mapping,
    STANDARD_MARKERS,
    SIMPLE_MARKERS,
    FILLED_UNFILLED_MARKERS,
    MARKER_SIZES,
    SIZE_RANGE_CATEGORICAL,
    SIZE_RANGE_CONTINUOUS,
    HATCH_PATTERNS,
)

__all__ = [
    # Color functions
    "get_palette",
    "list_palettes",
    "show_palette",
    "resolve_palette",
    # Color palettes
    "PASTEL_CATEGORICAL",
    "PASTEL_CATEGORICAL_MINIMAL",
    "PASTEL_SEQUENTIAL_GREEN",
    "PASTEL_SEQUENTIAL_BLUE",
    "PASTEL_SEQUENTIAL_PURPLE",
    "PASTEL_DIVERGING_RED_BLUE",
    "PASTEL_DIVERGING_GREEN_PURPLE",
    "PASTEL_SIGNIFICANCE",
    "PASTEL_POSITIVE_NEGATIVE",
    # Style functions
    "set_notebook_style",
    "set_publication_style",
    "set_illustrator_style",  # Backward compatibility alias
    "set_minimal_style",
    "set_poster_style",
    "reset_style",
    "get_current_style",
    "apply_custom_style",
    # Marker functions
    "get_marker_cycle",
    "get_hatch_cycle",
    "get_size_mapping",
    # Marker constants
    "STANDARD_MARKERS",
    "SIMPLE_MARKERS",
    "FILLED_UNFILLED_MARKERS",
    "MARKER_SIZES",
    "SIZE_RANGE_CATEGORICAL",
    "SIZE_RANGE_CONTINUOUS",
    "HATCH_PATTERNS",
]
