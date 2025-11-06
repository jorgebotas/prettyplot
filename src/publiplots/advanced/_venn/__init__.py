"""
Venn diagram module for publiplots.

This module provides functions for creating Venn diagrams for 2-6 sets.
Based on the pyvenn library by LankyCyril (https://github.com/LankyCyril/pyvenn).

The module exposes the internal implementation components and can be used
to create custom Venn diagram visualizations.
"""

from .core import draw_ellipse, draw_triangle, draw_text, init_axes, less_transparent_color
from .logic import generate_logics, generate_petal_labels, validate_dataset_dict, get_n_sets
from .diagram import draw_venn_diagram, draw_pseudovenn6, generate_colors
from .constants import (
    SHAPE_COORDS,
    SHAPE_DIMS,
    SHAPE_ANGLES,
    PETAL_LABEL_COORDS,
    PSEUDOVENN_PETAL_COORDS
)

__all__ = [
    # Core drawing functions
    'draw_ellipse',
    'draw_triangle',
    'draw_text',
    'init_axes',
    'less_transparent_color',
    # Logic functions
    'generate_logics',
    'generate_petal_labels',
    'validate_dataset_dict',
    'get_n_sets',
    # Diagram functions
    'draw_venn_diagram',
    'draw_pseudovenn6',
    'generate_colors',
    # Constants
    'SHAPE_COORDS',
    'SHAPE_DIMS',
    'SHAPE_ANGLES',
    'PETAL_LABEL_COORDS',
    'PSEUDOVENN_PETAL_COORDS',
]
