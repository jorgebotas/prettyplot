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
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle
import numpy as np

from ...config import DEFAULT_COLOR, DEFAULT_LINEWIDTH, DEFAULT_ALPHA


def _draw_intersection_bars(
    ax: Axes,
    sizes: List[int],
    positions: List[int],
    color: str = DEFAULT_COLOR,
    linewidth: float = DEFAULT_LINEWIDTH,
    alpha: float = 1.0,
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
        width=0.6,
        color=color,
        edgecolor="black",
        linewidth=linewidth,
        alpha=alpha,
        zorder=2,
    )

    # Style axes
    ax.set_xlim(-0.5, len(positions) - 0.5)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.8)
    ax.set_axisbelow(True)

    # Add value labels on top of bars
    for i, (pos, size) in enumerate(zip(positions, sizes)):
        ax.text(
            pos,
            size,
            str(size),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="normal",
        )


def _draw_set_size_bars(
    ax: Axes,
    set_names: List[str],
    set_sizes: Dict[str, int],
    positions: List[int],
    color: str = DEFAULT_COLOR,
    linewidth: float = DEFAULT_LINEWIDTH,
    alpha: float = 1.0,
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
        height=0.6,
        color=color,
        edgecolor="black",
        linewidth=linewidth,
        alpha=alpha,
        zorder=2,
    )

    # Style axes
    ax.set_ylim(-0.5, len(positions) - 0.5)
    ax.set_yticks(positions)
    ax.set_yticklabels(set_names, fontsize=11, fontweight="normal")
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.invert_xaxis()

    # Add value labels at end of bars
    max_size = max(sizes)
    for pos, size in zip(positions, sizes):
        ax.text(
            size,
            pos,
            f"  {size}",
            ha="right",
            va="center",
            fontsize=9,
            fontweight="normal",
        )


def _draw_matrix(
    ax: Axes,
    membership_matrix: List[Tuple[int, ...]],
    set_names: List[str],
    dot_size: float = 150,
    line_width: float = 2.5,
    active_color: str = "#2d2d2d",
    inactive_color: str = "#d0d0d0",
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
    line_width : float
        Width of connecting lines
    active_color : str
        Color for active set membership
    inactive_color : str
        Color for inactive dots
    """
    n_sets = len(set_names)
    n_intersections = len(membership_matrix)

    # Set positions (y-axis: one row per set)
    set_positions = list(range(n_sets))

    # Intersection positions (x-axis: one column per intersection)
    intersection_positions = list(range(n_intersections))

    # Draw dots for all positions
    for i, membership in enumerate(membership_matrix):
        active_sets = [j for j, is_member in enumerate(membership) if is_member]

        # Draw inactive dots (light gray)
        for j in range(n_sets):
            if j not in active_sets:
                ax.scatter(
                    i,
                    j,
                    s=dot_size * 0.4,
                    c=inactive_color,
                    marker="o",
                    zorder=2,
                    linewidths=0,
                )

        # Draw connecting line for active sets
        if len(active_sets) > 1:
            y_coords = active_sets
            x_coords = [i] * len(active_sets)
            ax.plot(
                x_coords,
                y_coords,
                color=active_color,
                linewidth=line_width,
                solid_capstyle="round",
                zorder=1,
            )

        # Draw active dots (dark)
        for j in active_sets:
            ax.scatter(
                i,
                j,
                s=dot_size,
                c=active_color,
                marker="o",
                edgecolors="black",
                linewidths=0.8,
                zorder=3,
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
            i + 0.5, color="#e0e0e0", linewidth=0.8, linestyle="-", zorder=0
        )


def setup_upset_axes(
    fig: plt.Figure,
    figsize: Optional[Tuple[float, float]] = None,
) -> Tuple[Axes, Axes, Axes]:
    """
    Set up the three-panel layout for UpSet plot.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure
    figsize : tuple, optional
        Figure size (width, height). If None, use default.

    Returns
    -------
    ax_intersections : Axes
        Axes for intersection size bars (top)
    ax_matrix : Axes
        Axes for membership matrix (middle)
    ax_sets : Axes
        Axes for set size bars (bottom left)
    """
    if figsize is not None:
        fig.set_size_inches(figsize)

    # Create grid spec with 3 rows, 2 columns
    # Layout:
    #   [intersection bars        ] (spans both columns)
    #   [matrix                   ] (right column only)
    #   [set bars] [empty/matrix  ] (left column = set bars)

    from matplotlib import gridspec

    # Define height ratios: intersection bars, matrix, set labels
    gs = gridspec.GridSpec(
        3,
        2,
        figure=fig,
        height_ratios=[2, 1.5, 0.1],  # Intersection bars taller than matrix
        width_ratios=[1, 4],  # Set bars narrower than matrix
        hspace=0.05,  # Small gap between intersection and matrix
        wspace=0.05,  # Small gap between set bars and matrix
    )

    # Top row: intersection bars (right column only, to align with matrix)
    ax_intersections = fig.add_subplot(gs[0, 1])

    # Middle row: matrix (right column)
    ax_matrix = fig.add_subplot(gs[1, 1])

    # Middle row: set bars (left column)
    ax_sets = fig.add_subplot(gs[1, 0])

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
        fig.suptitle(title, fontsize=14, fontweight="bold", y=0.98)

    if intersection_label:
        ax_intersections.set_ylabel(
            intersection_label, fontsize=11, fontweight="normal"
        )

    if set_label:
        ax_sets.set_xlabel(set_label, fontsize=11, fontweight="normal")
