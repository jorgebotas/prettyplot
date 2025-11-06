"""
Venn diagram module for publiplots.

This module provides functions for creating Venn diagrams for 2-6 sets.
Based on the pyvenn library by LankyCyril (https://github.com/LankyCyril/pyvenn).

The module exposes:
- Main API functions: venn() and pseudovenn()
- Internal implementation components for advanced use
"""

# Import main API functions from diagram
from .diagram import venn, pseudovenn

# Import internal components for advanced use
from .constants import (
    SHAPE_COORDS,
    SHAPE_DIMS,
    SHAPE_ANGLES,
    PETAL_LABEL_COORDS,
    PSEUDOVENN_PETAL_COORDS
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
    validate_dataset_dict,
    get_n_sets
)

# Export public API
__all__ = [
    # Main API functions
    'venn',
    'pseudovenn',
    # Internal components (for advanced use)
    'draw_ellipse',
    'draw_triangle',
    'draw_text',
    'init_axes',
    'less_transparent_color',
    'generate_logics',
    'generate_petal_labels',
    'validate_dataset_dict',
    'get_n_sets',
    'SHAPE_COORDS',
    'SHAPE_DIMS',
    'SHAPE_ANGLES',
    'PETAL_LABEL_COORDS',
    'PSEUDOVENN_PETAL_COORDS',
]
