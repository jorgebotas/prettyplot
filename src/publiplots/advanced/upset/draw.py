"""
Drawing utilities for UpSet plots.

This module handles the low-level rendering of UpSet plot components including
intersection bars, set size bars, and the membership matrix visualization.

Portions of this implementation are based on concepts from UpSetPlot:
https://github.com/jnothman/UpSetPlot
Copyright (c) 2016, Joel Nothman
Licensed under BSD-3-Clause
"""

from typing import Dict, List, Optional, Tuple
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import to_rgba

from publiplots.config import DEFAULT_COLOR, DEFAULT_LINEWIDTH, DEFAULT_ALPHA

GRID_LINEWIDTH = 1


def draw_intersection_bars(
    ax: Axes,
    sizes: List[int],
    positions: List[int],
    width: float = 0.6,
    color: str = DEFAULT_COLOR,
    linewidth: float = DEFAULT_LINEWIDTH,
    alpha: float = DEFAULT_ALPHA,
) -> None:
    """
    Draw bars showing intersection sizes.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes for the intersection size plot
    sizes : list of int
        Intersection sizes
    positions : list of int
        X positions for each bar
    width : float
        Width of the bars
    color : str
        Bar color
    linewidth : float
        Edge line width
    alpha : float
        Bar transparency
    """
    ax.bar(
        positions,
        sizes,
        width=width,
        color=to_rgba(color, alpha=alpha),
        edgecolor=color,
        linewidth=linewidth,
        zorder=2,
    )

    # Style axes
    ax.set_xlim(-0.5, len(positions) - 0.5)
    ax.set_xticks([])
    ax.set_ylim(-0.02 * max(sizes), 1.05 * max(sizes))
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--", linewidth=GRID_LINEWIDTH)
    ax.set_axisbelow(True)

    # Add value labels on top of bars
    for i, (pos, size) in enumerate(zip(positions, sizes)):
        ax.text(
            pos,
            size,
            str(size),
            ha="center",
            va="bottom",
        )


def draw_set_size_bars(
    ax: Axes,
    set_names: List[str],
    set_sizes: Dict[str, int],
    positions: List[int],
    width: float = 0.6,
    color: str = DEFAULT_COLOR,
    linewidth: float = DEFAULT_LINEWIDTH,
    alpha: float = DEFAULT_ALPHA,
) -> None:
    """
    Draw horizontal bars showing set sizes.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes for set size plot
    set_names : list
        Names of sets (bottom to top order)
    set_sizes : dict
        Mapping from set name to size
    positions : list
        Y positions for each bar
    width : float
        Width of the bars
    color : str
        Bar color
    linewidth : float
        Edge line width
    alpha : float
        Bar transparency
    """
    sizes = [set_sizes[name] for name in set_names]

    ax.barh(
        positions,
        sizes,
        height=width,
        color=to_rgba(color, alpha=alpha),
        edgecolor=color,
        linewidth=linewidth,
        zorder=2,
    )

    # Style axes
    ax.set_xlim(-0.02 * max(sizes), 1.05 * max(sizes))
    ax.set_ylim(-0.5, len(positions) - 0.5)
    ax.set_yticks(positions)
    ax.set_yticklabels(set_names, fontsize=matplotlib.rcParams["ytick.labelsize"])
    ax.tick_params(axis='y', which='both', left=False, right=False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--", linewidth=GRID_LINEWIDTH)
    ax.set_axisbelow(True)
    ax.invert_xaxis()

    # Add value labels at end of bars
    max_size = max(sizes)
    for name, pos, size in zip(set_names, positions, sizes):
        ax.text(
            size,
            pos,
            f"{name} ({size}) ",
            ha="right",
            va="center",
        )



def draw_matrix(
        ax: Axes,
        membership_matrix: List[Tuple[int, ...]],
        set_names: List[str],
        dot_size: float = 150,
        linewidth: float = DEFAULT_LINEWIDTH,
        active_color: str = DEFAULT_COLOR,
        inactive_color: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
    ) -> None:
    """
    Draw the membership matrix showing which sets each intersection contains.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes for matrix
    membership_matrix : list of tuples
        Binary membership patterns (each tuple is one column)
    set_names : list
        Names of sets (corresponds to rows, bottom to top)
    dot_size : float
        Size of dots in the matrix
    linewidth : float
        Width of connecting lines
    active_color : str, optional
        Color for active set membership. If None, use DEFAULT_COLOR.
    inactive_color : str, optional
        Color for inactive dots. If None, use to_rgba(color, alpha=alpha).
    """
    import numpy as np

    n_sets = len(set_names)
    n_intersections = len(membership_matrix)

    # Set positions (y-axis: one row per set)
    set_positions = list(range(n_sets))

    # Intersection positions (x-axis: one column per intersection)
    intersection_positions = list(range(n_intersections))

    # Set inactive color
    if inactive_color is None:
        inactive_color = to_rgba(DEFAULT_COLOR, alpha=alpha)

    # Set axis limits first (needed for transformation calculations)
    ax.set_xlim(-0.5, n_intersections - 0.5)
    ax.set_ylim(-0.5, n_sets - 0.5)

    # Draw dots for all positions
    for i, membership in enumerate(membership_matrix):
        active_sets = [j for j, is_member in enumerate(membership) if is_member]

        # Draw inactive dots (light gray)
        for j in range(n_sets):
            # Draw inactive dot
            ax.scatter(
                i,
                j,
                s=dot_size,
                color=inactive_color if j not in active_sets else "white",
                marker="o",
                zorder=2,
                linewidths=0,
            )

        x_coords = [i] * len(active_sets)
        y_coords = active_sets
        ax.plot(
            x_coords,
            y_coords,
            color=active_color,
            linewidth=linewidth,
            solid_capstyle="round",
            zorder=1,
        )

        # Draw active dots (dark)
        for j in active_sets:
            ax.scatter(
                i,
                j,
                s=dot_size,
                color=to_rgba(active_color, alpha=alpha),
                marker="o",
                edgecolors=active_color,
                linewidths=linewidth,
                zorder=4,
            )

    # Style axes
    ax.set_xlim(-0.5, n_intersections - 0.5)
    ax.set_ylim(-0.5, n_sets - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # Add horizontal grid lines between sets
    for i in range(n_sets - 1):
        ax.axhline(
            i + 0.5, 
            color="#e0e0e0", 
            linewidth=GRID_LINEWIDTH, 
            linestyle="-", 
            zorder=0
        )


def setup_upset_axes(
    fig: plt.Figure,
    set_names: List[str],
    n_intersections: int,
    figsize: Optional[Tuple[float, float]] = None,
    element_size: Optional[float] = None,
) -> Tuple[Axes, Axes, Axes]:
    """
    Set up the three-panel layout for UpSet plot with proper sizing.

    This function calculates figure dimensions to ensure:
    1. Set label text has enough space
    2. Each bar/dot column has equal width
    3. Intersection bars and set bars have the same width

    Parameters
    ----------
    fig : Figure
        Matplotlib figure
    set_names : list
        Names of sets (for measuring text width)
    n_intersections : int
        Number of intersections to display
    figsize : tuple, optional
        Figure size (width, height). If None, calculated automatically.
    element_size : float, optional
        Width of each element (bar/dot) in points. If None, calculated from figure width.

    Returns
    -------
    ax_intersections : Axes
        Axes for intersection size bars (top)
    ax_matrix : Axes
        Axes for membership matrix (middle)
    ax_sets : Axes
        Axes for set size bars (left)
    """
    import matplotlib
    from matplotlib import gridspec
    import numpy as np

    n_sets = len(set_names)

    # Measure text width needed for set labels
    text_kw = {"size": matplotlib.rcParams["ytick.labelsize"]}
    # Add "x" for margin
    t = fig.text(
        0,
        0,
        "\n".join(str(label) + "x" for label in set_names),
        **text_kw,
    )

    # Get text width in display coordinates
    fig.canvas.draw()  # Ensure renderer is available
    textw = t.get_window_extent(renderer=fig.canvas.get_renderer()).width
    t.remove()

    # Get figure width in display coordinates
    figw = fig.get_window_extent(renderer=fig.canvas.get_renderer()).width

    if figsize is None and element_size is None:
        # Calculate column width from available space
        # Reserve space for text labels
        colw = (figw - textw) / n_intersections

        # Calculate figure size to fit everything
        render_ratio = figw / fig.get_figwidth() if fig.get_figwidth() > 0 else 72

        # Ensure minimum element size
        if colw < 20:  # Minimum 20 points per column
            colw = 20
            figw = colw * n_intersections + textw
            fig.set_figwidth(figw / render_ratio)

        # Height: proportional to number of sets
        fig_height = max(6, n_sets * 0.8 + 3)  # 3 extra for intersection bars
        fig.set_figheight(fig_height)

    elif figsize is not None:
        # User specified figure size
        fig.set_size_inches(figsize)
        figw = fig.get_window_extent(renderer=fig.canvas.get_renderer()).width
        render_ratio = figw / fig.get_figwidth()
        colw = (figw - textw) / n_intersections

    else:
        # User specified element size
        render_ratio = figw / fig.get_figwidth() if fig.get_figwidth() > 0 else 72
        colw = element_size / 72 * render_ratio
        figw = colw * n_intersections + textw
        fig.set_figwidth(figw / render_ratio)
        fig.set_figheight((colw * n_sets) / render_ratio)

    # Calculate number of grid columns for text space
    text_cols = max(1, int(np.ceil(textw / colw)))

    # Create GridSpec with calculated proportions
    # Total columns: text_cols + n_intersections
    # Rows: intersection bars + matrix
    gs = gridspec.GridSpec(
        2,  # 2 rows: intersection bars (top) and matrix (bottom)
        text_cols + n_intersections,
        figure=fig,
        height_ratios=[2, n_sets],  # Intersection bars + matrix (one row per set)
        hspace=0.05,
        wspace=0,  # No space between columns - they're uniform
    )

    # Top row: intersection bars (only over the intersection columns)
    ax_intersections = fig.add_subplot(gs[0, text_cols:])

    # Bottom row left: set size bars (over text columns)
    ax_sets = fig.add_subplot(gs[1, :text_cols])

    # Bottom row right: matrix (over intersection columns)
    ax_matrix = fig.add_subplot(gs[1, text_cols:])

    return ax_intersections, ax_matrix, ax_sets


def add_upset_labels(
    fig: plt.Figure,
    ax_intersections: Axes,
    ax_sets: Axes,
    title: str = "",
    intersection_label: str = "Intersection Size",
    set_label: str = "Set Size",
) -> None:
    """
    Add labels and title to UpSet plot.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure
    ax_intersections : Axes
        Intersection size axes
    ax_sets : Axes
        Set size axes
    title : str
        Main plot title
    intersection_label : str
        Label for intersection size axis
    set_label : str
        Label for set size axis
    """
    if title:
        fig.suptitle(title, y=0.98)

    if intersection_label:
        ax_intersections.set_ylabel(
            intersection_label
        )

    if set_label:
        ax_sets.set_xlabel(set_label)
