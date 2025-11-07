"""
Main UpSet plot function.

This module provides the main user-facing upsetplot() function for creating
UpSet plot visualizations of set intersections.

Portions of this implementation are based on concepts from UpSetPlot:
https://github.com/jnothman/UpSetPlot
Copyright (c) 2016, Joel Nothman
Licensed under BSD-3-Clause
"""

from typing import Dict, Optional, Set, Tuple, Union
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import pandas as pd

from ...config import DEFAULT_COLOR, DEFAULT_LINEWIDTH, DEFAULT_ALPHA, DEFAULT_FIGSIZE
from .logic import process_upset_data
from .draw import (
    setup_upset_axes,
    _draw_intersection_bars,
    _draw_set_size_bars,
    _draw_matrix,
    add_upset_labels,
)


def upsetplot(
    data: Union[pd.DataFrame, pd.Series, Dict[str, Set]],
    sort_by: str = "size",
    ascending: bool = False,
    min_subset_size: Optional[int] = None,
    max_subset_size: Optional[int] = None,
    min_degree: int = 1,
    max_degree: Optional[int] = None,
    show_counts: int = 20,
    color: str = DEFAULT_COLOR,
    linewidth: float = DEFAULT_LINEWIDTH,
    alpha: float = 0.7,
    dot_size: float = 150,
    figsize: Optional[Tuple[float, float]] = None,
    title: str = "",
    intersection_label: str = "Intersection Size",
    set_label: str = "Set Size",
    fig: Optional[Figure] = None,
    **kwargs,
) -> Tuple[Figure, Tuple[Axes, Axes, Axes]]:
    """
    Create an UpSet plot for visualizing set intersections.

    UpSet plots are an effective way to visualize intersections of multiple sets,
    providing more clarity than Venn diagrams when dealing with many sets or
    complex intersection patterns.

    Parameters
    ----------
    data : DataFrame, Series, or dict of sets
        Input data in one of the following formats:

        - **DataFrame**: Each column represents a set, rows are elements.
          Values should be binary (0/1 or True/False) indicating membership.

        - **Series**: MultiIndex series where first level is elements and
          second level is sets, with binary values.

        - **dict**: Dictionary mapping set names (str) to sets of elements.
          Example: ``{'Set A': {1, 2, 3}, 'Set B': {2, 3, 4}}``

    sort_by : {'size', 'degree', 'name'}, default='size'
        How to sort intersections:

        - 'size': Sort by intersection size (largest first if ascending=False)
        - 'degree': Sort by number of sets in intersection
        - 'name': Sort alphabetically by set names

    ascending : bool, default=False
        Sort order. False shows largest/highest degree first.

    min_subset_size : int, optional
        Minimum size for an intersection to be displayed. Useful for
        filtering out small intersections.

    max_subset_size : int, optional
        Maximum size for an intersection to be displayed.

    min_degree : int, default=1
        Minimum number of sets in an intersection. Set to 2 to exclude
        individual sets.

    max_degree : int, optional
        Maximum number of sets in an intersection. Useful for focusing on
        simpler intersections.

    show_counts : int, default=20
        Maximum number of intersections to display in the plot.

    color : str, default=DEFAULT_COLOR
        Color for bars (both intersection and set size bars).
        Supports any matplotlib color specification.

    linewidth : float, default=DEFAULT_LINEWIDTH
        Width of edges around bars and dots in the matrix.

    alpha : float, default=0.7
        Transparency level for bars (0=transparent, 1=opaque).

    dot_size : float, default=150
        Size of dots in the membership matrix.

    figsize : tuple of (float, float), optional
        Figure size as (width, height) in inches. If None, uses a size
        based on the number of sets and intersections.

    title : str, default=""
        Main plot title.

    intersection_label : str, default="Intersection Size"
        Label for the y-axis of intersection size bars.

    set_label : str, default="Set Size"
        Label for the x-axis of set size bars.

    fig : Figure, optional
        Existing matplotlib Figure to use. If None, creates a new figure.

    **kwargs
        Additional keyword arguments (currently unused, reserved for future
        extensions).

    Returns
    -------
    fig : Figure
        Matplotlib Figure object.

    axes : tuple of (Axes, Axes, Axes)
        Tuple containing three axes:
        - ax_intersections: Intersection size bar plot (top)
        - ax_matrix: Set membership matrix (middle)
        - ax_sets: Set size bar plot (left)

    Notes
    -----
    UpSet plots consist of three main components:

    1. **Intersection size bars** (top): Show the number of elements in each
       intersection, sorted by the specified criterion.

    2. **Membership matrix** (middle): Visualizes which sets contribute to each
       intersection using dots and connecting lines. Each column represents one
       intersection, each row represents one set.

    3. **Set size bars** (left): Show the total size of each individual set.

    The implementation is inspired by the UpSetPlot package
    (https://github.com/jnothman/UpSetPlot) but redesigned to match the
    publiplots aesthetic with cleaner styling and integration with existing
    publiplots utilities.

    Examples
    --------
    Create an UpSet plot from a dictionary of sets:

    >>> data = {
    ...     'Set A': {1, 2, 3, 4, 5},
    ...     'Set B': {3, 4, 5, 6, 7},
    ...     'Set C': {5, 6, 7, 8, 9}
    ... }
    >>> fig, axes = upsetplot(data, title='Set Intersections')

    Create from a DataFrame with binary membership:

    >>> df = pd.DataFrame({
    ...     'Set A': [1, 1, 1, 0, 0],
    ...     'Set B': [0, 1, 1, 1, 0],
    ...     'Set C': [0, 0, 1, 1, 1]
    ... })
    >>> fig, axes = upsetplot(df, sort_by='degree', min_degree=2)

    Filter to show only intersections with at least 10 elements:

    >>> fig, axes = upsetplot(data, min_subset_size=10, show_counts=15)

    Customize colors and styling:

    >>> fig, axes = upsetplot(
    ...     data,
    ...     color='#ff6b6b',
    ...     alpha=0.8,
    ...     dot_size=200,
    ...     figsize=(12, 6)
    ... )

    See Also
    --------
    venn : Create Venn diagrams for 2-5 sets
    barplot : Create bar plots with grouping and styling
    scatterplot : Create scatter plots with size and color encoding

    References
    ----------
    .. [1] Lex et al. (2014). "UpSet: Visualization of Intersecting Sets".
       IEEE Transactions on Visualization and Computer Graphics.
    .. [2] UpSetPlot package: https://github.com/jnothman/UpSetPlot
    """
    # Process data
    processed = process_upset_data(
        data=data,
        sort_by=sort_by,
        ascending=ascending,
        min_subset_size=min_subset_size,
        max_subset_size=max_subset_size,
        min_degree=min_degree,
        max_degree=max_degree,
        show_counts=show_counts,
    )

    intersections = processed["intersections"]
    membership_matrix = processed["membership_matrix"]
    set_names = processed["set_names"]
    set_sizes = processed["set_sizes"]
    n_sets = processed["n_sets"]
    n_intersections = processed["n_intersections"]

    # Determine figure size if not provided
    if figsize is None:
        width = max(8, n_intersections * 0.4)
        height = max(6, n_sets * 0.5 + 3)
        figsize = (width, height)

    # Create figure
    if fig is None:
        fig = plt.figure(figsize=figsize)
    else:
        fig.set_size_inches(figsize)

    # Setup axes
    ax_intersections, ax_matrix, ax_sets = setup_upset_axes(fig, figsize=figsize)

    # Draw intersection size bars
    intersection_sizes = intersections["size"].tolist()
    intersection_positions = list(range(n_intersections))

    _draw_intersection_bars(
        ax=ax_intersections,
        sizes=intersection_sizes,
        positions=intersection_positions,
        color=color,
        linewidth=linewidth,
        alpha=alpha,
    )

    # Draw set size bars (reverse order for bottom-to-top display)
    set_positions = list(range(n_sets))

    _draw_set_size_bars(
        ax=ax_sets,
        set_names=set_names,
        set_sizes=set_sizes,
        positions=set_positions,
        color=color,
        linewidth=linewidth,
        alpha=alpha,
    )

    # Draw membership matrix
    _draw_matrix(
        ax=ax_matrix,
        membership_matrix=membership_matrix,
        set_names=set_names,
        dot_size=dot_size,
        line_width=linewidth * 1.2,
        active_color="#2d2d2d",
        inactive_color="#d0d0d0",
    )

    # Add labels and title
    add_upset_labels(
        fig=fig,
        ax_intersections=ax_intersections,
        ax_sets=ax_sets,
        title=title,
        intersection_label=intersection_label,
        set_label=set_label,
    )

    return fig, (ax_intersections, ax_matrix, ax_sets)
