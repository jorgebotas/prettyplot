"""
Venn diagram module for publiplots.

This module provides functions for creating Venn diagrams for 2-5 sets.
Re-engineered based on ggvenn R package (https://github.com/yanlinlin82/ggvenn).
Previously based on pyvenn library by LankyCyril.

The module exposes:
- Main API function: venn()
- Internal implementation components for advanced use
"""

# Import main API functions from diagram
from .diagram import venn

# Import internal components for advanced use
from .draw import (
    draw_ellipse,
    draw_text,
    init_axes,
)
from .logic import (
    generate_logics,
    generate_petal_labels,
    get_n_sets
)
from .geometry import (
    Circle,
    get_geometry,
    get_coordinate_ranges,
    generate_circle_2,
    generate_circle_3,
    generate_circle_4,
    generate_circle_5,
)

# Export public API
__all__ = [
    # Main API functions
    'venn',
    # Internal components (for advanced use)
    'draw_ellipse',
    'draw_text',
    'init_axes',
    'generate_logics',
    'generate_petal_labels',
    'get_n_sets',
    # Geometry components
    'Circle',
    'get_geometry',
    'get_coordinate_ranges',
    'generate_circle_2',
    'generate_circle_3',
    'generate_circle_4',
    'generate_circle_5',
]
