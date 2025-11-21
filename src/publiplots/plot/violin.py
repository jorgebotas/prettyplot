"""
Violin plot functions for publiplots.

This module provides publication-ready violin plot visualizations with
transparent fill and opaque edges.
"""

from typing import Optional, List, Dict, Tuple, Union

from publiplots.themes.rcparams import resolve_param
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import seaborn as sns
import pandas as pd

from publiplots.themes.colors import resolve_palette_map
from publiplots.utils.transparency import ArtistTracker


def violinplot(
    data: pd.DataFrame,
    x: Optional[str] = None,
    y: Optional[str] = None,
    hue: Optional[str] = None,
    order: Optional[List] = None,
    hue_order: Optional[List] = None,
    orient: Optional[str] = None,
    color: Optional[str] = None,
    palette: Optional[Union[str, Dict, List]] = None,
    saturation: float = 1.0,
    fill: bool = False,
    inner: Optional[str] = "box",
    split: bool = False,
    width: float = 0.8,
    dodge: Union[bool, str] = "auto",
    gap: float = 0,
    linewidth: Optional[float] = None,
    linecolor: str = "auto",
    cut: float = 2,
    gridsize: int = 100,
    bw_method: str = "scott",
    bw_adjust: float = 1,
    density_norm: str = "area",
    common_norm: bool = False,
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
    Create a publication-ready violin plot.

    This function creates violin plots with transparent fill and opaque edges,
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
        Fixed color for all violins (only used when hue is None).
    palette : str, dict, or list, optional
        Color palette for hue grouping.
    saturation : float, default=1.0
        Proportion of the original saturation to draw colors at.
    fill : bool, default=False
        Whether to fill the violin interior.
    inner : str, optional, default="box"
        Representation of the data in the violin interior.
        Options: "box", "quart", "point", "stick", None.
    split : bool, default=False
        When using hue nesting with a variable that takes two levels,
        setting split to True will draw half of a violin for each level.
    width : float, default=0.8
        Width of the violins.
    dodge : bool or "auto", default="auto"
        When hue nesting is used, whether elements should be shifted along
        the categorical axis.
    gap : float, default=0
        Gap between violins when using hue.
    linewidth : float, optional
        Width of violin edges.
    linecolor : str, default="auto"
        Color of violin edges.
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
    common_norm : bool, default=False
        When True, normalize across the entire dataset.
    alpha : float, optional
        Transparency of violin fill (0-1).
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
        Additional keyword arguments passed to seaborn.violinplot.

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Examples
    --------
    Simple violin plot:

    >>> import publiplots as pp
    >>> fig, ax = pp.violinplot(data=df, x="category", y="value")

    Violin plot with hue grouping:

    >>> fig, ax = pp.violinplot(
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

    # Prepare kwargs for seaborn violinplot
    violinplot_kwargs = {
        "data": data,
        "x": x,
        "y": y,
        "hue": hue,
        "order": order,
        "hue_order": hue_order,
        "orient": orient,
        "color": color if hue is None else None,
        "palette": palette if hue else None,
        "saturation": saturation,
        "fill": fill,
        "inner": inner,
        "split": split,
        "width": width,
        "dodge": dodge,
        "gap": gap,
        "linewidth": linewidth,
        "linecolor": linecolor,
        "cut": cut,
        "gridsize": gridsize,
        "bw_method": bw_method,
        "bw_adjust": bw_adjust,
        "density_norm": density_norm,
        "common_norm": common_norm,
        "ax": ax,
        "legend": False,  # Handle legend ourselves
    }

    # Merge with user-provided kwargs
    violinplot_kwargs.update(kwargs)

    # Track artists before plotting
    tracker = ArtistTracker(ax)

    # Create violinplot
    sns.violinplot(**violinplot_kwargs)

    # Apply transparency only to new violin collections
    tracker.apply_transparency(on="collections", face_alpha=alpha)

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
