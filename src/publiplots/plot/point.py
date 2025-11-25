"""
Point plot visualization module for publiplots.

Provides point plot (line plot with markers and error bars) visualizations
with support for categorical grouping and custom marker styling.
"""

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import to_rgba, Normalize
from matplotlib.cm import ScalarMappable
import numpy as np
import pandas as pd
from typing import Optional, Tuple, Union, Dict, List

from publiplots.themes.rcparams import resolve_param
from publiplots.themes.colors import resolve_palette_map
from publiplots.themes.markers import resolve_marker_map
from publiplots.utils import create_legend_handles, legend


def pointplot(
    data: pd.DataFrame,
    x: Optional[str] = None,
    y: Optional[str] = None,
    hue: Optional[str] = None,
    order: Optional[List] = None,
    hue_order: Optional[List] = None,
    estimator: str = "mean",
    errorbar: Optional[Union[str, Tuple]] = ("ci", 95),
    n_boot: int = 1000,
    seed: Optional[int] = None,
    units: Optional[str] = None,
    weights: Optional[str] = None,
    color: Optional[str] = None,
    palette: Optional[Union[str, Dict, List]] = None,
    markers: Optional[Union[bool, List[str], Dict[str, str]]] = None,
    linestyles: Optional[Union[str, List[str], Dict[str, str]]] = None,
    dodge: Union[bool, float] = False,
    orient: Optional[str] = None,
    capsize: float = 0,
    err_kws: Optional[Dict] = None,
    alpha: Optional[float] = None,
    linewidth: Optional[float] = None,
    markersize: Optional[float] = None,
    markeredgewidth: Optional[float] = None,
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
    Create a point plot with publiplots styling.

    Point plots show point estimates and error bars for numeric data
    grouped by categorical variables. Points are connected by lines to
    emphasize trends over categories. Markers use a distinctive double-layer
    style with white background and semi-transparent colored fill.

    Parameters
    ----------
    data : pd.DataFrame
        Input data containing x, y, and optional hue columns.
    x : str, optional
        Column name for x-axis (categorical).
    y : str, optional
        Column name for y-axis (numeric).
    hue : str, optional
        Column name for grouping variable that will produce lines with
        different colors and markers.
    order : list, optional
        Order to plot the categorical levels in.
    hue_order : list, optional
        Order to plot the hue levels in.
    estimator : str, default="mean"
        Statistical function to estimate within each categorical bin.
        Options: "mean", "median", etc.
    errorbar : str or tuple, default=("ci", 95)
        Method for computing error bars. Options include:
        - ("ci", confidence_level): Confidence interval
        - ("pi", confidence_level): Prediction interval
        - ("se", multiplier): Standard error with optional multiplier
        - "sd": Standard deviation
        - None: No error bars
    n_boot : int, default=1000
        Number of bootstrap iterations for computing confidence intervals.
    seed : int, optional
        Seed for random number generator.
    units : str, optional
        Column for sampling units (for nested data).
    weights : str, optional
        Column for observation weights.
    color : str, optional
        Fixed color for all points (only used when hue is None).
    palette : str, dict, list, or None
        Color palette for hue values:
        - str: palette name (e.g., "pastel")
        - dict: mapping of hue values to colors
        - list: list of colors
        - None: uses default palette
    markers : bool, list, dict, optional
        Markers to use for different hue levels:
        - True: use default marker set
        - list: list of marker symbols (e.g., ["o", "^", "s"])
        - dict: mapping of hue values to markers
        - None: uses default marker "o" for all points
    linestyles : str, list, dict, optional
        Line styles to use for different hue levels.
    dodge : bool or float, default=False
        Amount to separate points for different hue levels along the
        categorical axis.
    orient : str, optional
        Orientation of the plot ('v' or 'h').
    capsize : float, default=0
        Width of error bar caps.
    err_kws : dict, optional
        Additional keyword arguments for error bar styling.
        Example: {'linewidth': 1.5, 'alpha': 0.7}
    alpha : float, default=0.4
        Transparency level for marker fill (0-1).
    linewidth : float, default=2.0
        Width of marker edges and connecting lines.
    markersize : float, default=10
        Size of markers.
    markeredgewidth : float, default=1.0
        Width of marker edges.
    figsize : tuple, default=(6, 4)
        Figure size (width, height) if creating new figure.
    ax : Axes, optional
        Matplotlib axes object. If None, creates new figure.
    title : str, default=""
        Plot title.
    xlabel : str, default=""
        X-axis label. If empty, uses x column name.
    ylabel : str, default=""
        Y-axis label. If empty, uses y column name.
    legend : bool, default=True
        Whether to show legend.
    legend_kws : dict, optional
        Keyword arguments for legend builder:
        - hue_label : str, optional - Title for the hue legend.
    **kwargs
        Additional keyword arguments passed to seaborn.pointplot().

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Examples
    --------
    Simple point plot:
    >>> fig, ax = pp.pointplot(data=df, x="time", y="value")

    Point plot with grouping:
    >>> fig, ax = pp.pointplot(
    ...     data=df, x="time", y="value", hue="group",
    ...     palette={'Control': '#8E8EC1', 'Treated': '#75B375'}
    ... )

    Point plot with custom markers:
    >>> fig, ax = pp.pointplot(
    ...     data=df, x="time", y="value", hue="group",
    ...     markers=["o", "D"], errorbar="se"
    ... )
    """
    # Read defaults from rcParams if not provided
    figsize = resolve_param("figure.figsize", figsize)
    linewidth = resolve_param("lines.linewidth", linewidth)
    markersize = resolve_param("lines.markersize", markersize)
    markeredgewidth = resolve_param("lines.markeredgewidth", markeredgewidth)
    alpha = resolve_param("alpha", alpha)
    color = resolve_param("color", color)

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Resolve palette
    if hue is not None:
        hue_values = data[hue].unique() if hue_order is None else hue_order
        palette = resolve_palette_map(
            values=hue_values,
            palette=palette,
        )

    # Resolve markers
    if hue is not None and markers is None:
        markers = True

    if markers is True:
        # Get marker mapping
        hue_values = data[hue].unique() if hue_order is None else hue_order
        marker_map = resolve_marker_map(values=list(hue_values), marker_map=None)
        # Convert to list for seaborn
        markers = [marker_map[val] for val in hue_values]

    # Prepare err_kws with linewidth
    if err_kws is None:
        err_kws = {}
    if 'linewidth' not in err_kws:
        err_kws['linewidth'] = linewidth

    # Prepare kwargs for seaborn pointplot
    pointplot_kwargs = {
        "data": data,
        "x": x,
        "y": y,
        "hue": hue,
        "order": order,
        "hue_order": hue_order,
        "estimator": estimator,
        "errorbar": errorbar,
        "n_boot": n_boot,
        "seed": seed,
        "units": units,
        "weights": weights,
        "color": color if hue is None else None,
        "palette": palette if hue else None,
        "linewidth": linewidth,
        "markers": markers if hue else "o",
        "markersize": markersize,
        "markeredgewidth": markeredgewidth,
        "linestyles": linestyles,
        "dodge": dodge,
        "orient": orient,
        "capsize": capsize,
        "err_kws": err_kws,
        "ax": ax,
        "legend": False,  # Handle legend ourselves
    }

    # Merge with user-provided kwargs
    pointplot_kwargs.update(kwargs)

    # Create pointplot
    sns.pointplot(**pointplot_kwargs)

    # Apply marker styling (double-layer effect)
    _apply_marker_styling(
        ax=ax,
        alpha=alpha,
    )

    # Set labels
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)

    # Add legend if hue is used
    if legend and hue is not None:
        _legend(
            ax=ax,
            hue=hue,
            palette=palette,
            markers=markers,
            linestyles=linestyles,
            markersize=markersize,
            markeredgewidth=markeredgewidth,
            alpha=alpha,
            linewidth=linewidth,
            kwargs=legend_kws,
        )

    return fig, ax


def _apply_marker_styling(
    ax: Axes,
    alpha: float,
) -> List[Dict]:
    """
    Apply double-layer marker styling to pointplot.

    Extracts markers from lines, removes them, and redraws with:
    1. White background layer
    2. Semi-transparent colored fill layer

    Parameters
    ----------
    ax : Axes
        Axes containing the pointplot.
    alpha : float
        Transparency for marker fill.
    markeredgewidth : float
        Width of marker edges.

    """
    # Extract markers and line info from lines
    markers = []
    for line in ax.lines:
        marker = line.get_marker()
        if marker != "None":
            markers.append({
                'x': line.get_xdata(),
                'y': line.get_ydata(),
                'marker': marker,
                'color': line.get_color(),
                'markersize': line.get_markersize(),
                'linestyle': line.get_linestyle(),
                'linewidth': line.get_linewidth(),
                'markeredgewidth': line.get_markeredgewidth(),
            })
            # Remove marker from original line (keep the line itself)
            line.set_markersize(0)

    # Redraw markers with double-layer effect
    for data in markers:
        x = data['x']
        y = data['y']
        marker = data['marker']
        color = data['color']
        size = data['markersize']
        markeredgewidth = data['markeredgewidth'] 

        # Layer 1: White background (no edge)
        ax.plot(
            x, y, marker,
            markeredgecolor=color,
            markerfacecolor="white",
            markersize=size,
            markeredgewidth=0,
            linestyle='none',
            zorder=99
        )

        # Layer 2: Semi-transparent colored fill with edge
        ax.plot(
            x, y, marker,
            markeredgecolor=color,
            markerfacecolor=to_rgba(color, alpha),
            markersize=size,
            markeredgewidth=markeredgewidth,
            linestyle='none',
            zorder=100
        )


def _legend(
    ax: Axes,
    hue: str,
    palette: Union[Dict, str],
    markers: Union[List, Dict],
    linestyles: Union[List, Dict],
    markersize: Optional[float] = None,
    markeredgewidth: Optional[float] = None,
    alpha: Optional[float] = None,
    linewidth: Optional[float] = None,
    kwargs: Optional[Dict] = None,
) -> None:
    """
    Create legend handles for point plot.

    Parameters
    ----------
    ax : Axes
        Axes to create legend for.
    hue : str
        Hue column name.
    palette : dict or str
        Color palette mapping.
    markers : list or dict
        Marker symbols for each hue level.
    markersize : float, optional
        Marker size for legend markers.
    markeredgewidth : float, optional
        Marker edge width for legend markers.
    alpha : float, optional
        Transparency for legend markers.
    linewidth : float, optional
        Line width for legend markers.
    kwargs : dict, optional
        Additional legend customization.
    """
    # Read defaults from rcParams if not provided
    alpha = resolve_param("alpha", alpha)
    linewidth = resolve_param("lines.linewidth", linewidth)
    markersize = resolve_param("lines.markersize", markersize)
    markeredgewidth = resolve_param("lines.markeredgewidth", markeredgewidth)

    kwargs = kwargs or {}

    # Store legend data
    legend_data = {}

    # Extract unique hue values from marker_info
    if isinstance(palette, dict):
        # Use palette keys as the source of truth for labels
        labels = list(palette.keys())
        colors = list(palette.values())
        print(markersize)

        # Create legend handles with line+marker style
        hue_handles = create_legend_handles(
            labels=[str(label) for label in labels],
            colors=colors,
            markers=markers,
            linestyles=linestyles,
            alpha=alpha,
            linewidth=linewidth,
            sizes=[markersize],
            markeredgewidth=markeredgewidth,
        )

        legend_data["hue"] = {
            "handles": hue_handles,
            "label": kwargs.pop("hue_label", hue),
        }

    # Store metadata on first line for retrieval
    if len(ax.lines) > 0:
        ax.lines[0]._legend_data = legend_data

    # Create legend using legend() API
    builder = legend(ax=ax)
