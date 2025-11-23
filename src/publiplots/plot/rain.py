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


def rainplot(
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
    jitter: float = 0.05,
    # Offset control
    offset: float = 0.0,
    move: float = 0.0,
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
    orient : str, optional
        Orientation of the plot ('v' or 'h').
    color : str, optional
        Fixed color for all elements (only used when hue is None).
    palette : str, dict, or list, optional
        Color palette for hue grouping.
    saturation : float, default=1.0
        Proportion of the original saturation to draw colors at.
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
    jitter : float, default=0.05
        Amount of jitter for strip plot (ignored for swarm).
    offset : float, default=0.0
        Horizontal offset for the entire raincloud.
    move : float, default=0.0
        Additional offset for rain points from center.
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
    if orient is None:
        orient = "v"  # default vertical
    is_vertical = orient in ("v", "vertical")

    # Track all artists
    tracker = ArtistTracker(ax)

    # 1. Draw the half-violin (cloud)
    # Use the hue=True trick to create half-violin
    violin_kwargs = {
        "data": data,
        "x": x,
        "y": y,
        "hue": True,  # Trick for half-violin
        "hue_order": [True, False],  # Only True has data
        "order": order,
        "orient": orient,
        "color": color if hue is None else None,
        "palette": {True: color} if hue is None else None,
        "saturation": saturation,
        "fill": False,
        "inner": None,  # No inner elements in violin
        "split": True,
        "width": width,
        "linewidth": linewidth,
        "cut": cut,
        "gridsize": gridsize,
        "bw_method": bw_method,
        "bw_adjust": bw_adjust,
        "density_norm": density_norm,
        "ax": ax,
        "legend": False,
    }

    # Handle hue case - need to draw each hue level separately
    if hue is not None:
        hue_levels = hue_order if hue_order else data[hue].unique()
        cat_var = x if is_vertical else y
        categories = order if order else data[cat_var].unique()
        n_hue = len(hue_levels)

        for i, hue_val in enumerate(hue_levels):
            subset = data[data[hue] == hue_val]
            hue_color = palette[hue_val] if isinstance(palette, dict) else color

            # Calculate dodge offset for this hue level
            dodge_offset = (i - (n_hue - 1) / 2) * (width / n_hue)

            violin_kwargs_hue = violin_kwargs.copy()
            violin_kwargs_hue["data"] = subset
            violin_kwargs_hue["color"] = hue_color
            violin_kwargs_hue["palette"] = {True: hue_color}
            violin_kwargs_hue["width"] = width / n_hue * 0.9

            sns.violinplot(**violin_kwargs_hue)

            # Offset the violin collection
            if dodge_offset != 0:
                for coll in tracker.get_new_collections():
                    paths = coll.get_paths()
                    for path in paths:
                        if is_vertical:
                            path.vertices[:, 0] += dodge_offset
                        else:
                            path.vertices[:, 1] += dodge_offset
    else:
        sns.violinplot(**violin_kwargs)

    # Apply transparency to violin collections
    tracker.apply_transparency(on="collections", face_alpha=cloud_alpha)

    # 2. Draw box plot (umbrella) if requested
    if box:
        box_tracker = ArtistTracker(ax)

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
            "width": box_width,
            "whis": whis,
            "linewidth": linewidth,
            "fill": True,
            "ax": ax,
            "legend": False,
            "fliersize": 0,  # Hide outliers (shown as rain)
        }

        sns.boxplot(**boxplot_kwargs)

        # Set edge colors and apply transparency to box
        for patch in box_tracker.get_new_patches():
            patch.set_edgecolor(patch.get_facecolor())

        box_tracker.apply_transparency(on=["patches", "lines"], face_alpha=box_alpha)

    # 3. Draw rain (strip or swarm plot)
    if rain:
        rain_tracker = ArtistTracker(ax)

        if rain == "strip":
            rain_kwargs = {
                "data": data,
                "x": x,
                "y": y,
                "hue": hue,
                "order": order,
                "hue_order": hue_order,
                "orient": orient,
                "color": color if hue is None else None,
                "palette": palette if hue else None,
                "size": point_size,
                "jitter": jitter,
                "linewidth": linewidth * 0.5,
                "ax": ax,
                "legend": False,
                "dodge": hue is not None,
            }
            sns.stripplot(**rain_kwargs)
        elif rain == "swarm":
            rain_kwargs = {
                "data": data,
                "x": x,
                "y": y,
                "hue": hue,
                "order": order,
                "hue_order": hue_order,
                "orient": orient,
                "color": color if hue is None else None,
                "palette": palette if hue else None,
                "size": point_size,
                "linewidth": linewidth * 0.5,
                "ax": ax,
                "legend": False,
                "dodge": hue is not None,
            }
            sns.swarmplot(**rain_kwargs)

        # Offset rain points to the left of center
        rain_offset = -width / 4 - move
        for coll in rain_tracker.get_new_collections():
            offsets = coll.get_offsets()
            if is_vertical:
                offsets[:, 0] += rain_offset
            else:
                offsets[:, 1] += rain_offset
            coll.set_offsets(offsets)
            # Set edge colors
            coll.set_edgecolors(coll.get_facecolors())

        rain_tracker.apply_transparency(on="collections", face_alpha=rain_alpha)

    # Apply global offset if specified
    if offset != 0:
        for coll in ax.collections:
            if hasattr(coll, 'get_paths'):
                paths = coll.get_paths()
                for path in paths:
                    if is_vertical:
                        path.vertices[:, 0] += offset
                    else:
                        path.vertices[:, 1] += offset
            if hasattr(coll, 'get_offsets'):
                offsets = coll.get_offsets()
                if len(offsets) > 0:
                    if is_vertical:
                        offsets[:, 0] += offset
                    else:
                        offsets[:, 1] += offset
                    coll.set_offsets(offsets)

    # Add legend if hue is used
    if legend and hue is not None:
        from publiplots.utils.legend import legend as pp_legend
        from publiplots.utils.legend import create_legend_handles

        handles = create_legend_handles(
            labels=list(palette.keys()) if isinstance(palette, dict) else None,
            colors=list(palette.values()) if isinstance(palette, dict) else None,
            alpha=cloud_alpha,
            linewidth=linewidth,
        )

        legend_kwargs = legend_kws or dict(label=hue)
        pp_legend(ax, handles=handles, **legend_kwargs)

    # Set labels
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    return fig, ax
