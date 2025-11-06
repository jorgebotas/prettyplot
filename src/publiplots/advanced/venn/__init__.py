"""
Venn diagram module for publiplots.

This module provides functions for creating Venn diagrams for 2-6 sets.
Based on the pyvenn library by LankyCyril (https://github.com/LankyCyril/pyvenn).

The module exposes:
- Main API function: venn()
- Internal implementation components for advanced use
"""

# Import main API functions from diagram
from .diagram import venn

# Import internal components for advanced use
from .constants import (
    SHAPE_COORDS,
    SHAPE_DIMS,
    SHAPE_ANGLES,
    PETAL_LABEL_COORDS,
)
from .core import (
    draw_ellipse,
    draw_triangle,
    draw_text,
    init_axes,
    less_transparent_color
)
from .logic import (
    generate_logics,
    generate_petal_labels,
    get_n_sets
)

# Export public API
__all__ = [
    # Main API functions
    'venn',
    # Internal components (for advanced use)
    'draw_ellipse',
    'draw_triangle',
    'draw_text',
    'init_axes',
    'less_transparent_color',
    'generate_logics',
    'generate_petal_labels',
    'get_n_sets',
    'SHAPE_COORDS',
    'SHAPE_DIMS',
    'SHAPE_ANGLES',
    'PETAL_LABEL_COORDS',
]
