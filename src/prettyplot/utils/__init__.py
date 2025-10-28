"""
Utility functions for prettyplot.

This module provides helper functions for file I/O, axis manipulation,
and input validation.
"""

from prettyplot.utils.io import (
    savefig,
    save_multiple,
    close_all,
    get_figure_size,
    set_figure_size,
)

from prettyplot.utils.axes import (
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

from prettyplot.utils.validation import (
    validate_data,
    validate_numeric,
    validate_colors,
    validate_dimensions,
    validate_positive,
    validate_range,
    coerce_to_numeric,
    check_required_columns,
)

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
    "validate_data",
    "validate_numeric",
    "validate_colors",
    "validate_dimensions",
    "validate_positive",
    "validate_range",
    "coerce_to_numeric",
    "check_required_columns",
]
