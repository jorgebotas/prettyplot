"""
Box plot functions for publiplots.

This module provides publication-ready box plot visualizations with
transparent fill and opaque edges.
"""

from typing import Optional, List, Dict, Tuple, Union

from publiplots.themes.rcparams import resolve_param
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
import seaborn as sns
import pandas as pd
import numpy as np

from publiplots.themes.colors import resolve_palette_map
from publiplots.utils.transparency import apply_transparency
from publiplots.utils import is_categorical


def boxplot(
    data: pd.DataFrame,
    x: Optional[str] = None,
    y: Optional[str] = None,
    hue: Optional[str] = None,
    order: Optional[List] = None,
    hue_order: Optional[List] = None,
    orient: Optional[str] = None,
    color: Optional[str] = None,
    palette: Optional[Union[str, Dict, List]] = None,
    width: float = 0.8,
    gap: float = 0,
    whis: float = 1.5,
    fliersize: Optional[float] = None,
    linewidth: Optional[float] = None,
    alpha: Optional[float] = None,
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
    Create a publication-ready box plot.

    This function creates box plots with transparent fill and opaque edges,
    following the publiplots visual style.

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
    orient : str, optional
        Orientation of the plot ('v' or 'h').
    color : str, optional
        Fixed color for all boxes (only used when hue is None).
    palette : str, dict, or list, optional
        Color palette for hue grouping.
    width : float, default=0.8
        Width of the boxes.
    gap : float, default=0
        Gap between boxes when using hue.
    whis : float, default=1.5
        Proportion of IQR past low and high quartiles to extend whiskers.
    fliersize : float, optional
        Size of outlier markers.
    linewidth : float, optional
        Width of box edges.
    alpha : float, optional
        Transparency of box fill (0-1).
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
        Additional keyword arguments passed to seaborn.boxplot.

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Examples
    --------
    Simple box plot:

    >>> import publiplots as pp
    >>> fig, ax = pp.boxplot(data=df, x="category", y="value")

    Box plot with hue grouping:

    >>> fig, ax = pp.boxplot(
    ...     data=df, x="category", y="value", hue="group"
    ... )
    """
    # Read defaults from rcParams if not provided
    figsize = resolve_param("figure.figsize", figsize)
    linewidth = resolve_param("lines.linewidth", linewidth)
    alpha = resolve_param("alpha", alpha)
    color = resolve_param("color", color)

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

    # Determine categorical axis
    categorical_axis = "x"  # default
    if x is not None and y is not None:
        categorical_axis = "x" if is_categorical(data[x]) else "y"
    elif orient == "h":
        categorical_axis = "y"

    # Prepare kwargs for seaborn boxplot
    boxplot_kwargs = {
        "data": data,
        "x": x,
        "y": y,
        "hue": hue,
        "order": order,
        "hue_order": hue_order,
        "orient": orient,
        "color": color if hue is None else None,
        "palette": palette if hue else None,
        "width": width,
        "gap": gap,
        "whis": whis,
        "fliersize": fliersize,
        "linewidth": linewidth,
        "fill": True,  # Need fill=True to get patches
        "ax": ax,
        "legend": False,  # Handle legend ourselves
    }

    # Merge with user-provided kwargs
    boxplot_kwargs.update(kwargs)

    # Create boxplot
    sns.boxplot(**boxplot_kwargs)

    # Build a map of position -> color from patches
    # Position is on the categorical axis (x or y)
    patch_colors = {}
    for patch in ax.patches:
        verts = patch.get_path().vertices
        if categorical_axis == "x":
            pos = round(np.mean(verts[:, 0]), 2)
        else:
            pos = round(np.mean(verts[:, 1]), 2)
        patch_colors[pos] = patch.get_facecolor()

    # Resolve markeredgewidth for outliers
    flierprops = kwargs.get("flierprops", {})
    markeredgewidth = flierprops.get("markeredgewidth", None)
    markeredgewidth = resolve_param("lines.markeredgewidth", markeredgewidth)

    # Recolor all lines (whiskers, caps, medians, outliers) based on position
    for line in ax.lines:
        line_data = line.get_xdata() if categorical_axis == "x" else line.get_ydata()
        if len(line_data) == 0:
            continue
        pos = np.mean(line_data)
        # Find closest patch position
        closest_pos = min(patch_colors.keys(), key=lambda p: abs(p - pos))
        base_color = patch_colors[closest_pos]
        line.set_color(base_color)
        line.set_linewidth(linewidth)
        line.set_markeredgewidth(markeredgewidth)

    # Apply transparency to lines (outlier markers)
    apply_transparency(ax.lines, face_alpha=alpha, edge_alpha=1.0)

    # Set edge colors to match face colors
    for patch in ax.patches:
        patch.set_edgecolor(patch.get_facecolor())

    # Apply differential transparency to patches
    apply_transparency(ax.patches, face_alpha=alpha, edge_alpha=1.0)

    # Add legend if hue is used
    if legend and hue is not None:
        from publiplots.utils.legend import legend as pp_legend
        from publiplots.utils.legend import create_legend_handles

        handles = create_legend_handles(
            labels=list(palette.keys()) if isinstance(palette, dict) else None,
            colors=list(palette.values()) if isinstance(palette, dict) else None,
            alpha=alpha,
            linewidth=linewidth,
        )

        legend_kwargs = legend_kws or dict(label=hue)
        pp_legend(ax, handles=handles, **legend_kwargs)

    # Set labels
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)

    return fig, ax
