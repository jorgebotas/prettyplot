"""
Venn diagram visualizations for publiplots.

This module provides functions for creating Venn diagrams for 2-5 sets
using an implementation based on pyvenn by LankyCyril.

The module supports:
- Venn diagrams for 2-5 sets using ellipses

Based on pyvenn by LankyCyril: https://github.com/LankyCyril/pyvenn
"""

from matplotlib.axes import Axes
from typing import Dict, List, Optional, Tuple, Union

from publiplots.themes.rcparams import resolve_param
import matplotlib.pyplot as plt

from publiplots.themes.colors import get_palette

from .constants import (
    SHAPE_COORDS,
    SHAPE_DIMS,
    SHAPE_ANGLES,
    PETAL_LABEL_COORDS,
    SET_LABEL_COORDS,
    SET_LABEL_ALIGNMENTS
)
from .draw import (
    init_axes,
    draw_ellipse,
    draw_text,
)
from .logic import get_n_sets, generate_petal_labels


def _prepare_colors(colors, n_sets: int) -> Union[List[str], List[Tuple[float, ...]]]:
    """
    Prepare colors for Venn diagram sets.

    Parameters
    ----------
    colors : list, str, or None
        Colors specification (list of colors, colormap name, or None)
    n_sets : int
        Number of sets (2-5)

    Returns
    -------
    colors : list of str or tuple of floats (RGBA)
        List of color strings or RGBA tuples
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
    return color_list


def _venn(
    *,
    petal_labels: Dict[str, str],
    dataset_labels: List[str],
    colors: List[Tuple[float, ...]],
    alpha: float,
    figsize: Tuple[float, float],
    ax: Optional[Axes],
    color_labels: bool = True,
) -> Axes:
    """
    Draw a true Venn diagram with ellipses (2-5 sets).

    Internal function that handles the actual drawing logic.
    """
    n_sets = get_n_sets(petal_labels, dataset_labels)

    # Validate number of sets
    if n_sets < 2 or n_sets > 5:
        raise ValueError("Number of sets must be between 2 and 5. Consider using upset plot instead.")

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
        draw_ellipse(ax, *coords, *dims, angle, color, alpha=alpha)

    # Draw labels for each petal (intersection region)
    # Font size controlled by rcParams['font.size']
    for logic, petal_label in petal_labels.items():
        if logic in PETAL_LABEL_COORDS[n_sets]:
            x, y = PETAL_LABEL_COORDS[n_sets][logic]
            draw_text(ax, x, y, petal_label, fontsize=plt.rcParams['font.size'])

    # Draw set labels on diagram
    for i, label in enumerate(dataset_labels):
        x, y = SET_LABEL_COORDS[n_sets][i]
        ha, va = SET_LABEL_ALIGNMENTS[n_sets][i]
        color = colors[i] if color_labels else None
        draw_text(ax, x, y, label, fontsize=plt.rcParams['font.size'] * 1.2, color=color, ha=ha, va=va)

    return ax


# =============================================================================
# Public API
# =============================================================================


def venn(
    sets: Union[List[set], Dict[str, set]],
    labels: Optional[List[str]] = None,
    colors: Optional[Union[List[str], str]] = None,
    alpha: Optional[float] = None,
    figsize: Optional[Tuple[float, float]] = None,
    ax: Optional[Axes] = None,
    fmt: str = "{size}",
    color_labels: bool = True,
) -> Tuple[plt.Figure, Axes]:
    """
    Create a Venn diagram for 2-5 sets.

    This function creates true Venn diagrams that show all possible intersections.
    Each region (petal) is labeled with the size of the intersection by default.

    Parameters
    ----------
    sets : list of sets or dict
        Either a list of 2-5 sets, or a dictionary mapping labels to sets.
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
    color_labels : bool, default=True
        Whether to color the set labels with the same color as the petals.
    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Raises
    ------
    ValueError
        If the number of sets is not between 2 and 5
        Consider using upset plot instead.
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

    5-way Venn diagram with percentage labels:

    >>> fig, ax = pp.venn(
    ...     [set1, set2, set3, set4, set5],
    ...     fmt='{size} ({percentage:.1f}%)'
    ... )
    """
    # Read defaults from rcParams if not provided
    alpha = resolve_param("alpha", alpha)
    figsize = resolve_param("figure.figsize", figsize)

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
    if n_sets < 2 or n_sets > 5:
        raise ValueError("Venn diagram supports 2 to 5 sets. Consider using upset plot instead.")

    # Validate that all inputs are sets
    for s in sets_list:
        if not isinstance(s, set):
            raise TypeError("All elements must be sets")

    # Prepare colors using publiplots color utilities
    colors = _prepare_colors(colors, n_sets)

    # Generate petal labels (intersection sizes)
    petal_labels = generate_petal_labels(sets_list, fmt=fmt)

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Draw the Venn diagram
    ax = _venn(
        petal_labels=petal_labels,
        dataset_labels=labels,
        colors=colors,
        alpha=alpha,
        figsize=figsize,
        ax=ax,
        color_labels=color_labels,
    )

    return fig, ax