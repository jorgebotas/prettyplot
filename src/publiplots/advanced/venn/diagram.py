"""
Venn diagram visualizations for publiplots.

This module provides functions for creating Venn diagrams for 2-6 sets
using an implementation based on pyvenn by LankyCyril.

The module supports:
- True Venn diagrams for 2-6 sets (using ellipses for 2-5 sets, triangles for 6 sets)
- Pseudo-Venn diagrams for 6 sets (using overlapping circles)

Based on pyvenn by LankyCyril: https://github.com/LankyCyril/pyvenn
"""

from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from typing import Dict, List, Optional, Tuple, Union
from math import pi, sin, cos
import matplotlib.pyplot as plt

from publiplots.config import DEFAULT_ALPHA, DEFAULT_FIGSIZE
from publiplots.themes.colors import get_palette

from .constants import (
    SHAPE_COORDS,
    SHAPE_DIMS,
    SHAPE_ANGLES,
    PETAL_LABEL_COORDS,
    SET_LABEL_COORDS,
    SET_LABEL_ALIGNMENTS
)
from .core import init_axes, draw_ellipse, draw_triangle, draw_text
from .logic import get_n_sets, generate_petal_labels


def _prepare_colors(colors, n_sets: int, alpha: float) -> List[Tuple[float, ...]]:
    """
    Prepare RGBA color tuples for Venn diagram sets.

    Parameters
    ----------
    colors : list, str, or None
        Colors specification (list of colors, colormap name, or None)
    n_sets : int
        Number of sets (2-6)
    alpha : float
        Alpha transparency value

    Returns
    -------
    list of tuple
        List of RGBA color tuples
    """
    if colors is None:
        # Use default publiplots palette
        color_list = get_palette('pastel_categorical', n_colors=n_sets)
    elif isinstance(colors, str):
        # Use publiplots palette or colormap by name
        color_list = get_palette(colors, n_colors=n_sets)
    elif isinstance(colors, list):
        # Use provided color list
        color_list = colors[:n_sets]
    else:
        raise TypeError("colors must be None, a string (palette/colormap name), or a list of colors")

    # Convert to RGBA with specified alpha
    return [to_rgba(color, alpha=alpha) for color in color_list]


def _venn(
    *,
    petal_labels: Dict[str, str],
    dataset_labels: List[str],
    colors: List[Tuple[float, ...]],
    figsize: Tuple[float, float],
    set_labels: bool,
    ax: Optional[Axes]
) -> Axes:
    """
    Draw a true Venn diagram with ellipses (2-5 sets) or triangles (6 sets).

    Internal function that handles the actual drawing logic.
    """
    n_sets = get_n_sets(petal_labels, dataset_labels)

    # Determine which drawing function to use
    if 2 <= n_sets < 6:
        draw_shape = draw_ellipse
    elif n_sets == 6:
        draw_shape = draw_triangle
    else:
        raise ValueError("Number of sets must be between 2 and 6")

    # Initialize axes
    ax = init_axes(ax, figsize)

    # Draw all shapes
    shape_params = zip(
        SHAPE_COORDS[n_sets],
        SHAPE_DIMS[n_sets],
        SHAPE_ANGLES[n_sets],
        colors
    )
    for coords, dims, angle, color in shape_params:
        draw_shape(ax, *coords, *dims, angle, color)

    # Draw labels for each petal (intersection region)
    # Font size controlled by rcParams['font.size']
    for logic, petal_label in petal_labels.items():
        if logic in PETAL_LABEL_COORDS[n_sets]:
            x, y = PETAL_LABEL_COORDS[n_sets][logic]
            draw_text(ax, x, y, petal_label, fontsize=plt.rcParams['font.size'])

    # Draw set labels on diagram
    if set_labels:
        fontsize = plt.rcParams['font.size']
        for i, label in enumerate(dataset_labels):
            x, y = SET_LABEL_COORDS[n_sets][i]
            ha, va = SET_LABEL_ALIGNMENTS[n_sets][i]
            draw_text(ax, x, y, label, fontsize=fontsize * 1.2, color='black', ha=ha, va=va)

    return ax


def _pseudovenn(
    *,
    petal_labels: Dict[str, str],
    dataset_labels: List[str],
    colors: List[Tuple[float, ...]],
    figsize: Tuple[float, float],
    set_labels: bool,
    ax: Optional[Axes],
    hint_hidden: bool = True
) -> Axes:
    """
    Draw a pseudo-Venn diagram for 6 sets using overlapping circles.

    Internal function that handles the actual drawing logic.
    """
    n_sets = get_n_sets(petal_labels, dataset_labels)
    if n_sets != 6:
        raise NotImplementedError("Pseudovenn implemented only for 6 sets")

    # Initialize axes
    ax = init_axes(ax, figsize)

    # Draw 6 circles in a hexagonal pattern
    for step, color in enumerate(colors):
        angle = (2 - step) * pi / 3
        x = 0.5 + 0.2 * cos(angle)
        y = 0.5 + 0.2 * sin(angle)
        draw_ellipse(ax, x, y, 0.6, 0.6, 0, color)

    # Track hidden elements if hint_hidden is enabled
    if hint_hidden:
        hidden = [0] * n_sets

    # Draw labels for visible petals
    fontsize = plt.rcParams['font.size']
    for logic, petal_label in petal_labels.items():
        if logic in PSEUDOVENN_PETAL_COORDS[6]:
            x, y = PSEUDOVENN_PETAL_COORDS[6][logic]
            draw_text(ax, x, y, petal_label, fontsize=fontsize)
        elif hint_hidden:
            # Track hidden elements for each set
            for i, c in enumerate(logic):
                if c == "1":
                    hidden[i] += int(petal_label)

    # Display hints about hidden elements
    if hint_hidden:
        for step, hidden_value in enumerate(hidden):
            angle = (2 - step) * pi / 3
            x = 0.5 + 0.57 * cos(angle)
            y = 0.5 + 0.57 * sin(angle)
            draw_text(ax, x, y, f"{hidden_value}\n n/d*", fontsize=fontsize)

        # Adjust x-axis limit to accommodate hints
        ax.set(xlim=(-.2, 1.05))

        # Add explanation of the hint notation
        example_labels = list(dataset_labels)[0], list(dataset_labels)[3]
        hint_text = (
            "* elements of set in intersections that are not displayed,\n" +
            f"such as shared only between {example_labels[0]} and {example_labels[1]}"
        )
        draw_text(ax, 0.5, -0.1, hint_text, fontsize=fontsize)

    # Draw set labels on diagram
    if set_labels:
        fontsize = plt.rcParams['font.size']
        for i, label in enumerate(dataset_labels):
            x, y = SET_LABEL_COORDS[n_sets][i]
            ha, va = SET_LABEL_ALIGNMENTS[n_sets][i]
            draw_text(ax, x, y, label, fontsize=fontsize * 1.2, color='black', ha=ha, va=va)


    return ax


# =============================================================================
# Public API
# =============================================================================


def venn(
    sets: Union[List[set], Dict[str, set]],
    labels: Optional[List[str]] = None,
    colors: Optional[Union[List[str], str]] = None,
    alpha: float = DEFAULT_ALPHA,
    figsize: Tuple[float, float] = DEFAULT_FIGSIZE,
    ax: Optional[Axes] = None,
    set_labels: bool = True,
    fmt: str = "{size}"
) -> Tuple[plt.Figure, Axes]:
    """
    Create a Venn diagram for 2-6 sets.

    This function creates true Venn diagrams that show all possible intersections.
    For 2-5 sets, it uses ellipses; for 6 sets, it uses triangles. Each region
    (petal) is labeled with the size of the intersection by default.

    Parameters
    ----------
    sets : list of sets or dict
        Either a list of 2-6 sets, or a dictionary mapping labels to sets.
        Example: [set1, set2, set3] or {'A': set1, 'B': set2, 'C': set3}
    labels : list of str, optional
        Labels for each set. If sets is a dict, labels are taken from keys.
        Default: ['Set A', 'Set B', 'Set C', ...]
    colors : list of str, str, or None, optional
        Colors for each set. Can be:
        - List of color names/codes for each set
        - String name of a publiplots palette or matplotlib colormap
        - None (uses 'pastel_categorical' palette)
    alpha : float, default=0.3
        Transparency of set regions (0=transparent, 1=opaque).
    figsize : tuple, default=(10, 6)
        Figure size as (width, height) in inches.
    ax : Axes, optional
        Matplotlib axes object. If None, creates new figure.
    fmt : str, default='{size}'
        Format string for region labels. Can include:
        - {size}: number of elements in the intersection
        - {logic}: binary string representing the intersection
        - {percentage}: percentage of total elements

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Raises
    ------
    ValueError
        If the number of sets is not between 2 and 6
    TypeError
        If sets is not a list of sets or dict of sets

    Examples
    --------
    Simple 2-way Venn diagram:

    >>> set1 = {1, 2, 3, 4, 5}
    >>> set2 = {4, 5, 6, 7, 8}
    >>> fig, ax = pp.venn([set1, set2], labels=['Group A', 'Group B'])

    3-way Venn with custom colors:

    >>> sets_dict = {'A': set1, 'B': set2, 'C': set3}
    >>> colors = ['red', 'blue', 'green']
    >>> fig, ax = pp.venn(sets_dict, colors=colors)

    4-way Venn with colormap:

    >>> fig, ax = pp.venn([set1, set2, set3, set4], colors='Set1')

    6-way Venn diagram with percentage labels:

    >>> fig, ax = pp.venn(
    ...     [set1, set2, set3, set4, set5, set6],
    ...     fmt='{size} ({percentage:.1f}%)'
    ... )

    Notes
    -----
    - For 2-5 sets: Uses ellipses that show all possible intersections
    - For 6 sets: Uses overlapping circles (pseudo-Venn diagram), which does not show all possible intersections
    """
    # Parse input sets
    if isinstance(sets, dict):
        labels = list(sets.keys())
        sets_list = [set(s) for s in sets.values()]
    else:
        sets_list = [set(s) for s in sets]
        if labels is None:
            labels = [f"Set {chr(65+i)}" for i in range(len(sets_list))]

    # Validate number of sets
    n_sets = len(sets_list)
    if n_sets < 2 or n_sets > 6:
        raise ValueError("Venn diagram supports 2 to 6 sets")

    # Determine which drawing function to use
    draw_venn = _venn if n_sets <= 5 else _pseudovenn

    # Validate that all inputs are sets
    for s in sets_list:
        if not isinstance(s, set):
            raise TypeError("All elements must be sets")

    # Prepare colors using publiplots color utilities
    colors_rgba = _prepare_colors(colors, n_sets, alpha)

    # Generate petal labels (intersection sizes)
    petal_labels = generate_petal_labels(sets_list, fmt=fmt)

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Draw the Venn diagram
    ax = draw_venn(
        petal_labels=petal_labels,
        dataset_labels=labels,
        colors=colors_rgba,
        figsize=figsize,
        ax=ax,
        set_labels=set_labels,
    )

    return fig, ax