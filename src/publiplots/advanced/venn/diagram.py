"""
Main Venn diagram drawing functions.

This module provides the high-level functions for drawing Venn diagrams and
pseudovenn diagrams, coordinating the drawing primitives with set logic.

Adapted from pyvenn by LankyCyril (https://github.com/LankyCyril/pyvenn)
"""

from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from matplotlib.cm import ScalarMappable
from typing import Dict, List, Optional, Tuple
from math import pi, sin, cos

from .constants import (
    SHAPE_COORDS,
    SHAPE_DIMS,
    SHAPE_ANGLES,
    PETAL_LABEL_COORDS,
    PSEUDOVENN_PETAL_COORDS
)
from .core import init_axes, draw_ellipse, draw_triangle, draw_text
from .logic import get_n_sets


def generate_colors(cmap="viridis", n_colors: int = 6, alpha: float = 0.4) -> List[Tuple[float, ...]]:
    """
    Generate colors from matplotlib colormap or use provided color list.

    This function creates a list of RGBA colors either by sampling from a matplotlib
    colormap or by converting a provided list of colors to RGBA format with the
    specified alpha value.

    Parameters
    ----------
    cmap : str or list, default='viridis'
        If string: name of a matplotlib colormap to sample from
        If list: list of color specifications to convert to RGBA
    n_colors : int, default=6
        Number of colors to generate (must be between 2 and 6)
    alpha : float, default=0.4
        Transparency level for the colors (0=transparent, 1=opaque)

    Returns
    -------
    list of tuple
        List of RGBA color tuples, each containing (red, green, blue, alpha)
        values in the range [0, 1]

    Raises
    ------
    ValueError
        If n_colors is not an integer between 2 and 6

    Examples
    --------
    >>> colors = generate_colors('viridis', n_colors=3, alpha=0.5)
    >>> len(colors)
    3

    >>> colors = generate_colors(['red', 'blue', 'green'], n_colors=3, alpha=0.3)
    >>> # Returns 3 RGBA tuples with alpha=0.3
    """
    if not isinstance(n_colors, int) or (n_colors < 2) or (n_colors > 6):
        raise ValueError("n_colors must be an integer between 2 and 6")

    if isinstance(cmap, list):
        colors = [to_rgba(color, alpha=alpha) for color in cmap]
    else:
        scalar_mappable = ScalarMappable(cmap=cmap)
        colors = scalar_mappable.to_rgba(range(n_colors), alpha=alpha).tolist()

    return colors[:n_colors]


def draw_venn_diagram(
    *,
    petal_labels: Dict[str, str],
    dataset_labels: List[str],
    colors: List[Tuple[float, ...]],
    figsize: Tuple[float, float],
    fontsize: int,
    legend_loc: Optional[str],
    ax: Optional[Axes]
) -> Axes:
    """
    Draw a true Venn diagram with ellipses (2-5 sets) or triangles (6 sets).

    This function creates the actual Venn diagram by drawing the shapes for each set
    and annotating each region with its corresponding label (typically the size of
    the intersection).

    Parameters
    ----------
    petal_labels : dict
        Dictionary mapping binary logic strings to label text for each region
    dataset_labels : list of str
        Names/labels for each dataset to show in the legend
    colors : list of tuple
        RGBA color tuples for each set
    figsize : tuple of float
        Figure size as (width, height) in inches
    fontsize : int
        Font size for labels in points
    legend_loc : str or None
        Location for the legend (e.g., 'upper right'). If None, no legend is drawn.
    ax : matplotlib.axes.Axes or None
        Axes to draw on. If None, new axes are created.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the Venn diagram

    Raises
    ------
    ValueError
        If the number of sets is not between 2 and 6

    Notes
    -----
    - For 2-5 sets: Uses ellipses as shapes
    - For 6 sets: Uses triangles as shapes (true Venn diagram)
    - Not all petal positions may be available in the PETAL_LABEL_COORDS,
      in which case those labels are simply not drawn
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
    for logic, petal_label in petal_labels.items():
        # Some petals might not have predefined positions
        if logic in PETAL_LABEL_COORDS[n_sets]:
            x, y = PETAL_LABEL_COORDS[n_sets][logic]
            draw_text(ax, x, y, petal_label, fontsize=fontsize)

    # Add legend if requested
    if legend_loc is not None:
        ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})

    return ax


def draw_pseudovenn6(
    *,
    petal_labels: Dict[str, str],
    dataset_labels: List[str],
    colors: List[Tuple[float, ...]],
    figsize: Tuple[float, float],
    fontsize: int,
    legend_loc: Optional[str],
    ax: Optional[Axes],
    hint_hidden: bool = True
) -> Axes:
    """
    Draw a pseudo-Venn diagram for 6 sets using overlapping circles.

    Unlike the true Venn diagram which uses triangles, this creates an intersection
    of 6 circles. This is more visually intuitive but does not display all possible
    intersections (63 total). Hidden intersections can be indicated with hints.

    Parameters
    ----------
    petal_labels : dict
        Dictionary mapping binary logic strings to label text for each region
    dataset_labels : list of str
        Names/labels for each dataset to show in the legend
    colors : list of tuple
        RGBA color tuples for each set
    figsize : tuple of float
        Figure size as (width, height) in inches
    fontsize : int
        Font size for labels in points
    legend_loc : str or None
        Location for the legend (e.g., 'upper right'). If None, no legend is drawn.
    ax : matplotlib.axes.Axes or None
        Axes to draw on. If None, new axes are created.
    hint_hidden : bool, default=True
        If True, displays hints showing the total size of non-displayed intersections
        for each set

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the pseudo-Venn diagram

    Raises
    ------
    NotImplementedError
        If n_sets is not exactly 6

    Notes
    -----
    - Only works for exactly 6 sets
    - Uses 6 overlapping circles arranged in a hexagonal pattern
    - Does not show all 63 possible intersections
    - When hint_hidden=True, shows "n/d*" annotations indicating hidden elements,
      where n is the number of elements in non-displayed intersections for that set
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
    for logic, petal_label in petal_labels.items():
        # Not all intersections are shown in pseudovenn
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

    # Add legend if requested
    if legend_loc is not None:
        ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})

    return ax
