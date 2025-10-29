"""
Scatterplot visualization module for prettyplot.

Provides flexible scatterplot visualizations with support for both continuous
and categorical data, size encoding, and color encoding (categorical or continuous).
"""

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
from typing import Optional, Tuple, Union, Dict, List

from prettyplot.config import DEFAULT_FIGSIZE, DEFAULT_ALPHA, DEFAULT_LINEWIDTH
from prettyplot.themes.colors import resolve_palette, DEFAULT_COLOR


def scatterplot(
    data: pd.DataFrame,
    x: str,
    y: str,
    size: Optional[str] = None,
    hue: Optional[str] = None,
    color: Optional[str] = None,
    palette: Optional[Union[str, Dict, List]] = None,
    sizes: Optional[Tuple[float, float]] = None,
    size_norm: Optional[Tuple[float, float]] = None,
    hue_norm: Optional[Tuple[float, float]] = None,
    alpha: float = DEFAULT_ALPHA,
    linewidth: float = DEFAULT_LINEWIDTH,
    edgecolor: Optional[str] = None,
    style: str = "double",
    figsize: Tuple[float, float] = DEFAULT_FIGSIZE,
    ax: Optional[Axes] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    legend: Union[bool, str] = "auto",
    **kwargs
) -> Tuple[plt.Figure, Axes]:
    """
    Create a scatterplot with prettyplot styling.

    This function creates scatterplots for both continuous and categorical data
    with extensive customization options. Supports size and color encoding,
    with distinctive double-layer markers for enhanced visibility.

    Parameters
    ----------
    data : pd.DataFrame
        Input data containing x, y, and optional size/hue columns.
    x : str
        Column name for x-axis values (continuous or categorical).
    y : str
        Column name for y-axis values (continuous or categorical).
    size : str, optional
        Column name for marker sizes. If None, all markers have the same size.
    hue : str, optional
        Column name for marker colors. Can be categorical or continuous.
        If None, uses DEFAULT_COLOR or the value from `color` parameter.
    color : str, optional
        Fixed color for all markers (only used when hue is None).
        Overrides DEFAULT_COLOR. Example: '#ff0000' or 'red'.
    palette : str, dict, list, or None
        Color palette for hue values:
        - str: palette name (e.g., 'viridis', 'pastel_categorical')
        - dict: mapping of hue values to colors (categorical only)
        - list: list of colors
        - None: uses default palette
    sizes : tuple of float, optional
        (min_size, max_size) in points^2 for marker sizes.
        Default: (50, 500) for continuous data, (100, 100) for no size encoding.
    size_norm : tuple of float, optional
        (vmin, vmax) for size normalization. If None, computed from data.
    hue_norm : tuple of float, optional
        (vmin, vmax) for continuous hue normalization. If None, computed from data.
        Providing this enables continuous color mapping.
    alpha : float, default=0.1
        Transparency level for marker fill (0-1).
    linewidth : float, default=2.0
        Width of marker edges.
    edgecolor : str, optional
        Color for marker edges. If None, uses same color as fill.
    style : str, default='double'
        Marker style: 'double' for filled + edge layers, 'single' for standard.
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
    legend : bool or str, default='auto'
        Whether to show legend. Options: True, False, 'auto' (show if hue or size used).
    **kwargs
        Additional keyword arguments passed to seaborn.scatterplot().

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Examples
    --------
    Simple scatterplot with continuous data:
    >>> fig, ax = pp.scatterplot(data=df, x='time', y='value')

    Scatterplot with size encoding:
    >>> fig, ax = pp.scatterplot(data=df, x='time', y='value',
    ...                           size='magnitude', sizes=(50, 500))

    Scatterplot with categorical color encoding:
    >>> fig, ax = pp.scatterplot(data=df, x='time', y='value',
    ...                           hue='group', palette='pastel_categorical')

    Scatterplot with continuous color encoding:
    >>> fig, ax = pp.scatterplot(data=df, x='time', y='value',
    ...                           hue='score', palette='viridis',
    ...                           hue_norm=(0, 100))

    Scatterplot with custom single color:
    >>> fig, ax = pp.scatterplot(data=df, x='time', y='value',
    ...                           color='#e67e7e')

    Categorical scatterplot (positions on grid):
    >>> fig, ax = pp.scatterplot(data=df, x='category', y='condition',
    ...                           size='pvalue', hue='log2fc')

    See Also
    --------
    circle_heatmap : Specialized scatterplot for categorical heatmaps with
                     extensive legend customization.
    """
    # Validate required columns
    required_cols = [x, y]
    if size is not None:
        required_cols.append(size)
    if hue is not None:
        required_cols.append(hue)

    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in data: {missing_cols}")

    # Copy data to avoid modifying original
    plot_data = data.copy()

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Determine if x and y are categorical
    x_is_categorical = pd.api.types.is_categorical_dtype(plot_data[x]) or \
                       pd.api.types.is_object_dtype(plot_data[x]) or \
                       isinstance(plot_data[x].iloc[0], str)
    y_is_categorical = pd.api.types.is_categorical_dtype(plot_data[y]) or \
                       pd.api.types.is_object_dtype(plot_data[y]) or \
                       isinstance(plot_data[y].iloc[0], str)

    # Handle categorical positioning
    if x_is_categorical or y_is_categorical:
        plot_data, x_col, y_col, x_labels, y_labels = _handle_categorical_axes(
            plot_data, x, y, x_is_categorical, y_is_categorical
        )
    else:
        x_col, y_col = x, y
        x_labels, y_labels = None, None

    # Determine color/palette to use
    plot_color = None
    plot_palette = None
    plot_hue = hue

    if hue is None:
        # No hue encoding - use single color
        plot_color = color if color is not None else DEFAULT_COLOR
    else:
        # Hue encoding - use palette
        # Determine if hue is continuous
        is_continuous_hue = (
            hue_norm is not None or
            pd.api.types.is_numeric_dtype(plot_data[hue])
        )

        if palette is None:
            # Use default palette
            if is_continuous_hue:
                plot_palette = 'viridis'
            else:
                n_colors = plot_data[hue].nunique()
                plot_palette = resolve_palette(None, n_colors=n_colors)
        elif isinstance(palette, str):
            # Resolve string palette
            if is_continuous_hue:
                plot_palette = palette
            else:
                n_colors = plot_data[hue].nunique()
                plot_palette = resolve_palette(palette, n_colors=n_colors)
        else:
            # Use provided palette as-is (dict or list)
            plot_palette = palette

    # Set default sizes
    if sizes is None:
        if size is not None:
            sizes = (50, 500)
        else:
            sizes = (100, 100)

    # Create normalization for hue if needed
    if hue is not None and hue_norm is not None:
        hue_norm_obj = Normalize(vmin=hue_norm[0], vmax=hue_norm[1])
    else:
        hue_norm_obj = None

    # Prepare kwargs for seaborn scatterplot
    scatter_kwargs = {
        'data': plot_data,
        'x': x_col,
        'y': y_col,
        'ax': ax,
        'legend': False,  # We'll handle legend ourselves
    }

    # Add optional parameters
    if size is not None:
        scatter_kwargs['size'] = size
        scatter_kwargs['sizes'] = sizes
    else:
        scatter_kwargs['s'] = sizes[0]

    if plot_hue is not None:
        scatter_kwargs['hue'] = plot_hue
        scatter_kwargs['palette'] = plot_palette
        if hue_norm_obj is not None:
            scatter_kwargs['hue_norm'] = hue_norm_obj
    else:
        scatter_kwargs['color'] = plot_color

    # Merge with user kwargs
    scatter_kwargs.update(kwargs)

    # Create the plot based on style
    if style == 'double':
        # Double marker style (fill + edge)
        # Layer 1: Filled markers with transparency
        fill_kwargs = scatter_kwargs.copy()
        fill_kwargs['alpha'] = alpha
        fill_kwargs['edgecolor'] = 'none'
        fill_kwargs['linewidth'] = 0
        fill_kwargs['zorder'] = 2
        sns.scatterplot(**fill_kwargs)

        # Layer 2: Edge-only markers
        edge_kwargs = scatter_kwargs.copy()
        edge_kwargs['alpha'] = 1.0
        edge_kwargs['linewidth'] = linewidth
        edge_kwargs['zorder'] = 3
        sns.scatterplot(**edge_kwargs)

        # Make second layer hollow
        collections = ax.collections
        if len(collections) >= 2:
            edge_collection = collections[-1]
            face_collection = collections[-2]
            edge_collection.set_facecolors('none')
            edge_collection.set_edgecolors(
                edgecolor if edgecolor else face_collection.get_facecolors()
            )
            edge_collection.set_linewidths(linewidth)
    else:
        # Single marker style (standard)
        scatter_kwargs['alpha'] = alpha if alpha > 0.1 else 0.6
        scatter_kwargs['linewidth'] = linewidth
        if edgecolor:
            scatter_kwargs['edgecolor'] = edgecolor
        sns.scatterplot(**scatter_kwargs)

    # Handle categorical axis labels
    if x_labels is not None:
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels)
    if y_labels is not None:
        ax.set_yticks(range(len(y_labels)))
        ax.set_yticklabels(y_labels)

    # Set labels
    ax.set_xlabel(xlabel if xlabel else x)
    ax.set_ylabel(ylabel if ylabel else y)
    ax.set_title(title)

    # Handle legend
    show_legend = legend
    if legend == 'auto':
        show_legend = (hue is not None) or (size is not None)

    if show_legend and (hue is not None or size is not None):
        # Let seaborn create default legend
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(handles, labels, bbox_to_anchor=(1.01, 1), loc='upper left',
                     frameon=False)

    return fig, ax


def _handle_categorical_axes(
    data: pd.DataFrame,
    x: str,
    y: str,
    x_is_categorical: bool,
    y_is_categorical: bool
) -> Tuple[pd.DataFrame, str, str, Optional[List], Optional[List]]:
    """
    Handle categorical axes by creating position mappings.

    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    x : str
        X column name.
    y : str
        Y column name.
    x_is_categorical : bool
        Whether x is categorical.
    y_is_categorical : bool
        Whether y is categorical.

    Returns
    -------
    data : pd.DataFrame
        Data with added position columns.
    x_col : str
        Column name to use for x plotting.
    y_col : str
        Column name to use for y plotting.
    x_labels : list or None
        X-axis labels if categorical.
    y_labels : list or None
        Y-axis labels if categorical.
    """
    data = data.copy()

    if x_is_categorical:
        x_cats = sorted(data[x].unique())
        x_positions = {cat: i for i, cat in enumerate(x_cats)}
        data['_x_pos'] = data[x].map(x_positions)
        x_col = '_x_pos'
        x_labels = x_cats
    else:
        x_col = x
        x_labels = None

    if y_is_categorical:
        y_cats = sorted(data[y].unique())
        y_positions = {cat: i for i, cat in enumerate(y_cats)}
        data['_y_pos'] = data[y].map(y_positions)
        y_col = '_y_pos'
        y_labels = y_cats
    else:
        y_col = y
        y_labels = None

    return data, x_col, y_col, x_labels, y_labels
