"""
Venn diagram visualizations for publiplots.

This module provides functions for creating Venn diagrams for 2-6 sets
using an implementation based on pyvenn by LankyCyril.

The module supports:
- True Venn diagrams for 2-6 sets (using ellipses for 2-5 sets, triangles for 6 sets)
- Pseudo-Venn diagrams for 6 sets (using overlapping circles)
"""

from typing import Optional, Dict, List, Union, Tuple
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from publiplots.config import DEFAULT_ALPHA, DEFAULT_FIGSIZE
from publiplots.themes.colors import get_palette
from .diagram import generate_colors, draw_venn_diagram, draw_pseudovenn6
from .logic import generate_petal_labels


def venn(
    sets: Union[List[set], Dict[str, set]],
    labels: Optional[List[str]] = None,
    colors: Optional[Union[List[str], str]] = None,
    weighted: bool = False,
    alpha: float = DEFAULT_ALPHA,
    figsize: Tuple[float, float] = DEFAULT_FIGSIZE,
    ax: Optional[Axes] = None,
    fontsize: int = 13,
    legend_loc: str = "upper right",
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
        - String name of a matplotlib colormap
        - None (uses 'viridis' colormap)
    weighted : bool, default=False
        If True, attempts to scale regions proportionally to set sizes.
        Note: This is not fully supported in the current implementation and may
        not produce accurate proportional scaling. Future versions will improve this.
    alpha : float, default=0.3
        Transparency of set regions (0=transparent, 1=opaque).
    figsize : tuple, default=(10, 6)
        Figure size as (width, height) in inches.
    ax : Axes, optional
        Matplotlib axes object. If None, creates new figure.
    fontsize : int, default=13
        Font size for labels in points.
    legend_loc : str, default='upper right'
        Location for the legend. Standard matplotlib legend locations are supported.
        Set to None to hide the legend.
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
    >>> colors = pp.get_palette('pastel_categorical', n_colors=3)
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
    - For 6 sets: Uses triangles to show all 63 possible intersections
    - The 'weighted' parameter is provided for API compatibility but does not
      currently produce accurate proportional scaling
    - Based on pyvenn by LankyCyril (https://github.com/LankyCyril/pyvenn)

    See Also
    --------
    pseudovenn : Alternative 6-set visualization using circles (doesn't show all intersections)
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

    # Validate that all inputs are sets
    for s in sets_list:
        if not isinstance(s, set):
            raise TypeError("All elements must be sets")

    # Get colors
    if colors is None:
        # Use default palette if not specified
        colors_rgba = generate_colors(
            cmap=get_palette('pastel_categorical', n_colors=n_sets),
            n_colors=n_sets,
            alpha=alpha
        )
    elif isinstance(colors, str):
        # Use colormap name
        colors_rgba = generate_colors(cmap=colors, n_colors=n_sets, alpha=alpha)
    elif isinstance(colors, list):
        # Use provided color list
        colors_rgba = generate_colors(cmap=colors, n_colors=n_sets, alpha=alpha)
    else:
        raise TypeError("colors must be None, a string (colormap name), or a list of colors")

    # Generate petal labels (intersection sizes)
    petal_labels = generate_petal_labels(sets_list, fmt=fmt)

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Draw the Venn diagram
    ax = draw_venn_diagram(
        petal_labels=petal_labels,
        dataset_labels=labels,
        colors=colors_rgba,
        figsize=figsize,
        fontsize=fontsize,
        legend_loc=legend_loc,
        ax=ax
    )

    plt.tight_layout()
    return fig, ax


def pseudovenn(
    sets: Union[List[set], Dict[str, set]],
    labels: Optional[List[str]] = None,
    colors: Optional[Union[List[str], str]] = None,
    alpha: float = DEFAULT_ALPHA,
    figsize: Tuple[float, float] = DEFAULT_FIGSIZE,
    ax: Optional[Axes] = None,
    fontsize: int = 13,
    legend_loc: str = "upper right",
    fmt: str = "{size}",
    hint_hidden: bool = True
) -> Tuple[plt.Figure, Axes]:
    """
    Create a pseudo-Venn diagram for 6 sets using overlapping circles.

    Unlike the true Venn diagram which uses triangles for 6 sets, this function
    creates an intersection of 6 circles arranged in a hexagonal pattern. This
    is more visually intuitive but does not display all 63 possible intersections.
    Hidden intersections can be indicated with hints.

    Parameters
    ----------
    sets : list of sets or dict
        Either a list of exactly 6 sets, or a dictionary mapping labels to 6 sets.
    labels : list of str, optional
        Labels for each set. If sets is a dict, labels are taken from keys.
        Default: ['Set A', 'Set B', 'Set C', 'Set D', 'Set E', 'Set F']
    colors : list of str, str, or None, optional
        Colors for each set. Can be:
        - List of color names/codes for each set
        - String name of a matplotlib colormap
        - None (uses 'viridis' colormap)
    alpha : float, default=0.3
        Transparency of set regions (0=transparent, 1=opaque).
    figsize : tuple, default=(10, 6)
        Figure size as (width, height) in inches.
    ax : Axes, optional
        Matplotlib axes object. If None, creates new figure.
    fontsize : int, default=13
        Font size for labels in points.
    legend_loc : str, default='upper right'
        Location for the legend. Standard matplotlib legend locations are supported.
        Set to None to hide the legend.
    fmt : str, default='{size}'
        Format string for region labels. Can only use '{size}' when hint_hidden=True.
        When hint_hidden=False, can also use:
        - {logic}: binary string representing the intersection
        - {percentage}: percentage of total elements
    hint_hidden : bool, default=True
        If True, displays hints showing the total size of non-displayed intersections
        for each set (shown as "n/d*" where n is the number of hidden elements).

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Raises
    ------
    ValueError
        If the number of sets is not exactly 6
    TypeError
        If sets is not a list of sets or dict of sets
    NotImplementedError
        If hint_hidden=True and fmt is not '{size}'

    Examples
    --------
    Basic pseudo-Venn for 6 sets:

    >>> sets_list = [set1, set2, set3, set4, set5, set6]
    >>> fig, ax = pp.pseudovenn(sets_list)

    With custom labels and colors:

    >>> sets_dict = {'A': set1, 'B': set2, 'C': set3, 'D': set4, 'E': set5, 'F': set6}
    >>> fig, ax = pp.pseudovenn(sets_dict, colors='Set2')

    Without hidden element hints:

    >>> fig, ax = pp.pseudovenn(sets_list, hint_hidden=False, fmt='{size} ({percentage:.1f}%)')

    Notes
    -----
    - Only works for exactly 6 sets
    - Uses 6 overlapping circles in a hexagonal arrangement
    - Does not show all 63 possible intersections (only ~32 are visible)
    - When hint_hidden=True, annotations show how many elements from each set
      are in non-displayed intersections
    - Based on pyvenn by LankyCyril (https://github.com/LankyCyril/pyvenn)

    See Also
    --------
    venn : True Venn diagram that shows all intersections (uses triangles for 6 sets)
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
    if n_sets != 6:
        raise ValueError("Pseudo-Venn diagram requires exactly 6 sets. Use venn() for 2-5 sets.")

    # Validate that all inputs are sets
    for s in sets_list:
        if not isinstance(s, set):
            raise TypeError("All elements must be sets")

    # Validate fmt with hint_hidden
    if hint_hidden and fmt != "{size}":
        raise NotImplementedError(f"To use fmt='{fmt}', set hint_hidden=False")

    # Get colors
    if colors is None:
        colors_rgba = generate_colors(
            cmap=get_palette('pastel_categorical', n_colors=6),
            n_colors=6,
            alpha=alpha
        )
    elif isinstance(colors, str):
        colors_rgba = generate_colors(cmap=colors, n_colors=6, alpha=alpha)
    elif isinstance(colors, list):
        colors_rgba = generate_colors(cmap=colors, n_colors=6, alpha=alpha)
    else:
        raise TypeError("colors must be None, a string (colormap name), or a list of colors")

    # Generate petal labels
    petal_labels = generate_petal_labels(sets_list, fmt=fmt)

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Draw the pseudo-Venn diagram
    ax = draw_pseudovenn6(
        petal_labels=petal_labels,
        dataset_labels=labels,
        colors=colors_rgba,
        figsize=figsize,
        fontsize=fontsize,
        legend_loc=legend_loc,
        ax=ax,
        hint_hidden=hint_hidden
    )

    plt.tight_layout()
    return fig, ax
