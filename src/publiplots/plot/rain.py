"""
Rain plot (raincloud plot) functions for publiplots.

This module provides publication-ready raincloud plot visualizations that
combine half-violin plots, box plots, and strip/swarm plots.
"""

from typing import Optional, List, Dict, Tuple, Union

from publiplots.themes.rcparams import resolve_param
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import seaborn as sns
import pandas as pd
import numpy as np

from publiplots.themes.colors import resolve_palette_map
from publiplots.utils.transparency import ArtistTracker
from publiplots.utils.validation import is_categorical
from publiplots.plot.violin import violinplot
from publiplots.plot.box import boxplot
from publiplots.plot.swarm import swarmplot


def rainplot(
    data: pd.DataFrame,
    x: Optional[str] = None,
    y: Optional[str] = None,
    hue: Optional[str] = None,
    order: Optional[List] = None,
    hue_order: Optional[List] = None,
    color: Optional[str] = None,
    palette: Optional[Union[str, Dict, List]] = None,
    saturation: float = 1.0,
    dodge: bool = True,
    gap: float = 0.3,
    # Violin (cloud) parameters
    cloud_alpha: Optional[float] = None,
    width: float = 0.6,
    cut: float = 2,
    gridsize: int = 100,
    bw_method: str = "scott",
    bw_adjust: float = 1,
    density_norm: str = "area",
    # Box parameters
    box: bool = True,
    box_width: float = 0.15,
    box_alpha: Optional[float] = None,
    whis: float = 1.5,
    # Points (rain) parameters
    rain: str = "strip",
    rain_alpha: Optional[float] = 0.6,
    point_size: float = 3,
    # Offset control
    box_offset: float = 0.0,
    rain_offset: float = -0.15,
    # General styling
    linewidth: Optional[float] = None,
    figsize: Optional[Tuple[float, float]] = None,
    ax: Optional[Axes] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    legend: bool = True,
    legend_kws: Optional[Dict] = None,
    **kwargs
) -> Tuple[plt.Figure, Axes]:
    """
    Create a publication-ready raincloud plot.

    A raincloud plot combines a half-violin plot (cloud), a box plot (umbrella),
    and a strip/swarm plot (rain) to show both the distribution and individual
    data points.

    Parameters
    ----------
    data : DataFrame
        Input data.
    x : str, optional
        Column name for x-axis variable.
    y : str, optional
        Column name for y-axis variable.
    hue : str, optional
        Column name for color grouping.
    order : list, optional
        Order for the categorical levels.
    hue_order : list, optional
        Order for the hue levels.
    color : str, optional
        Fixed color for all elements (only used when hue is None).
    palette : str, dict, or list, optional
        Color palette for hue grouping.
    saturation : float, default=1.0
        Proportion of the original saturation to draw colors at.
    dodge : bool, default=True
        Whether to dodge the violin and box plot.
    gap : float, default=0.3
        Gap between the violin and the box plot.
    cloud_alpha : float, optional
        Transparency of violin fill (0-1). Defaults to rcParams alpha.
    width : float, default=0.6
        Width of the violin.
    cut : float, default=2
        Distance past extreme data points to extend density estimate.
    gridsize : int, default=100
        Number of points in the discrete grid used to evaluate KDE.
    bw_method : str, default="scott"
        Method for calculating smoothing bandwidth.
    bw_adjust : float, default=1
        Factor to adjust the bandwidth.
    density_norm : str, default="area"
        Method for normalizing density ("area", "count", "width").
    box : bool, default=True
        Whether to show the box plot.
    box_width : float, default=0.15
        Width of the box plot.
    box_alpha : float, optional
        Transparency of box fill. Defaults to cloud_alpha.
    whis : float, default=1.5
        Proportion of IQR past low and high quartiles to extend whiskers.
    rain : str, default="strip"
        Type of point plot for rain. Options: "strip", "swarm", or None.
    rain_alpha : float, default=0.6
        Transparency of rain points.
    point_size : float, default=3
        Size of rain points.
    box_offset : float, default=0.0
        Offset for the box plot from center position.
    rain_offset : float, default=-0.15
        Offset for rain points from center position. Negative values move
        points to the left (for vertical) or down (for horizontal).
    linewidth : float, optional
        Width of edges.
    figsize : tuple, optional
        Figure size (width, height) if creating new figure.
    ax : Axes, optional
        Matplotlib axes object. If None, creates new figure.
    title : str, default=""
        Plot title.
    xlabel : str, default=""
        X-axis label.
    ylabel : str, default=""
        Y-axis label.
    legend : bool, default=True
        Whether to show the legend.
    legend_kws : dict, optional
        Additional keyword arguments for legend.
    **kwargs
        Additional keyword arguments.

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Examples
    --------
    Simple raincloud plot:

    >>> import publiplots as pp
    >>> fig, ax = pp.rainplot(data=df, x="category", y="value")

    Raincloud plot with hue grouping:

    >>> fig, ax = pp.rainplot(
    ...     data=df, x="category", y="value", hue="group"
    ... )
    """
    # Read defaults from rcParams if not provided
    figsize = resolve_param("figure.figsize", figsize)
    linewidth = resolve_param("lines.linewidth", linewidth)
    cloud_alpha = resolve_param("alpha", cloud_alpha)
    color = resolve_param("color", color)

    if box_alpha is None:
        box_alpha = cloud_alpha

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Resolve palette
    if hue is not None:
        palette = resolve_palette_map(
            values=data[hue].unique(),
            palette=palette,
        )

    # Determine orientation
    is_vertical = is_categorical(data[x])

    # 1. Draw the half-violin (cloud) using pp.violinplot with side parameter
    violinplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        order=order,
        hue_order=hue_order,
        color=color,
        palette=palette,
        saturation=saturation,
        inner=None,
        width=width,
        dodge=dodge,
        linewidth=linewidth,
        cut=cut,
        gap=gap,
        gridsize=gridsize,
        bw_method=bw_method,
        bw_adjust=bw_adjust,
        density_norm=density_norm,
        alpha=cloud_alpha,
        ax=ax,
        legend=True,
        side="right",
    )

    # 2. Draw box plot (umbrella) if requested
    if box:
        box_tracker = ArtistTracker(ax)
        boxplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            order=order,
            hue_order=hue_order,
            color=color if hue is None else None,
            palette=palette if hue else None,
            width=width,
            gap=(1 - box_width),
            whis=whis,
            linewidth=linewidth,
            ax=ax,
            legend=False,
            fliersize=0,
        )

        # Apply box offset
        if box_offset != 0:
            # Offset patches (box bodies) - modify path vertices
            for patch in box_tracker.get_new_patches():
                path = patch.get_path()
                if is_vertical:
                    path.vertices[:, 0] += box_offset
                else:
                    path.vertices[:, 1] += box_offset
            # Offset lines (whiskers, medians, caps)
            for line in box_tracker.get_new_lines():
                if is_vertical:
                    line.set_xdata(line.get_xdata() + box_offset)
                else:
                    line.set_ydata(line.get_ydata() + box_offset)

    # 3. Draw rain (strip or swarm plot)
    if rain:
        rain_tracker = ArtistTracker(ax)
        swarmplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            order=order,
            hue_order=hue_order,
            color=color if hue is None else None,
            palette=palette if hue else None,
            alpha=rain_alpha,
            size=point_size,
            linewidth=linewidth * 0.5,
            ax=ax,
            legend=False,
            dodge=dodge,
        )

        # Apply rain offset
        for coll in rain_tracker.get_new_collections():
            offsets = coll.get_offsets()
            if is_vertical:
                offsets[:, 0] += rain_offset
            else:
                offsets[:, 1] += rain_offset
            coll.set_offsets(offsets)

    # Set labels
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)

    return fig, ax
