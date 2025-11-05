"""
Utility functions for prettyplots.

This module provides helper functions for file I/O, axis manipulation,
and input validation.
"""

from prettyplots.utils.io import (
    savefig,
    save_multiple,
    close_all,
    get_figure_size,
    set_figure_size,
)

from prettyplots.utils.axes import (
    adjust_spines,
    add_grid,
    remove_grid,
    set_axis_labels,
    set_axis_limits,
    rotate_xticklabels,
    rotate_yticklabels,
    invert_axis,
    add_reference_line,
    set_aspect_equal,
    tighten_layout,
)

from prettyplots.utils.validation import (
    is_categorical,
    is_numeric,
    validate_data,
    validate_numeric,
    validate_colors,
    validate_dimensions,
    validate_positive,
    validate_range,
    coerce_to_numeric,
    check_required_columns,
)

from prettyplots.utils.fonts import (
    _register_fonts,
    list_registered_fonts,
)

from prettyplots.utils.legend import (
    HandlerCircle,
    HandlerRectangle,
    get_legend_handler_map,
    create_legend_handles,
    LegendBuilder,
    create_legend_builder,
)

# Register fonts globally
_register_fonts()

__all__ = [
    # I/O functions
    "savefig",
    "save_multiple",
    "close_all",
    "get_figure_size",
    "set_figure_size",
    # Axes functions
    "adjust_spines",
    "add_grid",
    "remove_grid",
    "set_axis_labels",
    "set_axis_limits",
    "rotate_xticklabels",
    "rotate_yticklabels",
    "invert_axis",
    "add_reference_line",
    "set_aspect_equal",
    "tighten_layout",
    # Validation functions
    "is_categorical",
    "is_numeric",
    "validate_data",
    "validate_numeric",
    "validate_colors",
    "validate_dimensions",
    "validate_positive",
    "validate_range",
    "coerce_to_numeric",
    "check_required_columns",
    # Fonts functions
    "list_registered_fonts",
    # Legend functions
    "HandlerCircle",
    "HandlerRectangle",
    "get_legend_handler_map",
    "create_legend_handles",
    "LegendBuilder",
    "create_legend_builder",
]
