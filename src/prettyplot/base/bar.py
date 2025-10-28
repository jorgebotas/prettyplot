"""
Bar plot functions for prettyplot.

This module provides publication-ready bar plot visualizations with
flexible styling and grouping options.
"""

from typing import Optional, List, Dict, Tuple, Union
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import seaborn as sns
import pandas as pd
import numpy as np

from prettyplot.config import DEFAULT_LINEWIDTH, DEFAULT_ALPHA, DEFAULT_CAPSIZE, DEFAULT_FIGSIZE
from prettyplot.themes.colors import resolve_palette, DEFAULT_COLOR


def barplot(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: Optional[str] = None,
    split: Optional[str] = None,
    ax: Optional[Axes] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    linewidth: float = DEFAULT_LINEWIDTH,
    capsize: float = DEFAULT_CAPSIZE,
    alpha: float = DEFAULT_ALPHA,
    figsize: Tuple[float, float] = DEFAULT_FIGSIZE,
    palette: Optional[Union[str, Dict, List]] = None,
    hatch_mapping: Optional[Dict[str, str]] = None,
    errorbar: str = "se",
    gap: float = 0.1,
    order: Optional[List[str]] = None,
    split_order: Optional[List[str]] = None,
    **kwargs
) -> Tuple[plt.Figure, Axes]:
    """
    Create a publication-ready bar plot.

    This function creates bar plots with optional grouping, error bars,
    and hatch patterns. Supports both simple and complex bar plots with
    side-by-side grouped bars.

    Parameters
    ----------
    data : DataFrame
        Input data.
    x : str
        Column name for x-axis categories.
    y : str
        Column name for y-axis values.
    hue : str, optional
        Column name for color grouping (typically same as x for split bars).
    split : str, optional
        Column name for splitting bars side-by-side with hatch patterns.
        When specified, creates grouped bars within each x category.
    ax : Axes, optional
        Matplotlib axes object. If None, creates new figure.
    title : str, default=""
        Plot title.
    xlabel : str, default=""
        X-axis label. If empty and split is used, uses x column name.
    ylabel : str, default=""
        Y-axis label. If empty, uses y column name.
    linewidth : float, default=2.0
        Width of bar edges.
    capsize : float, default=0.0
        Width of error bar caps.
    alpha : float, default=0.1
        Transparency of bar fill (0-1). Use 0 for outlined bars only.
    figsize : tuple, default=(4, 4)
        Figure size (width, height) if creating new figure.
    palette : str, dict, or list, optional
        Color palette. Can be:
        - str: seaborn palette name or prettyplot palette name
        - dict: mapping from hue values to colors
        - list: list of colors
    hatch_mapping : dict, optional
        Mapping from split values to hatch patterns.
        Example: {'group1': '', 'group2': '///', 'group3': '\\\\\\'}
    errorbar : str, default='se'
        Error bar type: 'se' (standard error), 'sd' (standard deviation),
        'ci' (confidence interval), or None for no error bars.
    gap : float, default=0.1
        Gap between bar groups (0-1).
    order : list, optional
        Order of x-axis categories.
    split_order : list, optional
        Order of split categories. If provided, determines bar order within groups.
    **kwargs
        Additional keyword arguments passed to seaborn.barplot().

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.

    Examples
    --------
    Simple bar plot:
    >>> fig, ax = pp.barplot(data=df, x='category', y='value')

    Bar plot with color groups:
    >>> fig, ax = pp.barplot(data=df, x='category', y='value',
    ...                       hue='group', palette='pastel_categorical')

    Bar plot with split bars and hatch patterns:
    >>> fig, ax = pp.barplot(
    ...     data=df, x='condition', y='measurement',
    ...     split='treatment', hue='condition',
    ...     hatch_mapping={'control': '', 'treated': '///'},
    ...     palette={'A': '#75b375', 'B': '#8e8ec1'}
    ... )

    See Also
    --------
    barplot_enrichment : Specialized bar plot for enrichment analysis
    """
    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Resolve palette (handles prettyplot and seaborn palettes)
    resolved_palette = None
    bar_color = None

    # Determine if we need to use color or palette
    has_grouping = hue is not None or split is not None

    if has_grouping:
        # When there's grouping (hue or split), use palette
        if isinstance(palette, str) or palette is None:
            # Determine number of colors needed based on hue or split
            if hue is not None:
                n_colors = data[hue].nunique()
            else:  # split is not None
                n_colors = data[x].nunique()
            resolved_palette = resolve_palette(palette, n_colors=n_colors)
        else:
            resolved_palette = palette
    else:
        # When there's no grouping, use a single color
        if palette is None:
            # Use default color
            bar_color = DEFAULT_COLOR
        elif isinstance(palette, str):
            # Resolve the palette and use the first color
            colors = resolve_palette(palette, n_colors=1)
            bar_color = colors[0] if isinstance(colors, list) else list(colors.values())[0]
        elif isinstance(palette, list):
            # Use the first color from the list
            bar_color = palette[0]
        elif isinstance(palette, dict):
            # Use the first color from the dict
            bar_color = list(palette.values())[0]

    plot_data = data.copy()

    # Handle split bars (side-by-side grouped bars)
    if split is not None:
        plot_data = _prepare_split_data(
            plot_data, x, y, split, split_order=split_order
        )
        plot_x = '_plot_group'

        # Create default hatch mapping if not provided
        if hatch_mapping is None:
            split_values = data[split].unique()
            hatch_mapping = _create_default_hatch_mapping(split_values)
    else:
        plot_x = x

    # Apply order to x categories if specified
    if order is not None:
        plot_data[x] = pd.Categorical(plot_data[x], categories=order, ordered=True)

    # Prepare kwargs for seaborn barplot
    barplot_kwargs = {
        'data': plot_data,
        'x': plot_x,
        'y': y,
        'fill': False,
        'linewidth': linewidth,
        'capsize': capsize,
        'ax': ax,
        'err_kws': {"linewidth": linewidth},
        'errorbar': errorbar,
        'gap': gap,
        'legend': False,
    }

    # Add hue if split is used, otherwise only if explicitly provided
    if split is not None:
        barplot_kwargs['hue'] = x
    elif hue is not None:
        barplot_kwargs['hue'] = hue

    # Add palette or color
    if resolved_palette is not None:
        barplot_kwargs['palette'] = resolved_palette
    elif bar_color is not None:
        barplot_kwargs['color'] = bar_color

    # Merge with user-provided kwargs
    barplot_kwargs.update(kwargs)

    # Create outline bars
    sns.barplot(**barplot_kwargs)

    # Add filled bars with alpha if needed
    if 0 < alpha < 1:
        fill_kwargs = barplot_kwargs.copy()
        fill_kwargs.update({
            'fill': True,
            'alpha': alpha,
            'linewidth': 0,
            'err_kws': {"linewidth": 0},
        })
        sns.barplot(**fill_kwargs)

    # Apply hatch patterns if split is used
    if split is not None:
        _apply_hatch_to_bars(
            ax=ax,
            data=data,
            split_col=split,
            hatch_mapping=hatch_mapping,
        )

        # Clean up x-axis labels to show only main categories
        _fix_split_xticks(ax, plot_data, data, x, split)

    # Set labels
    ax.set_xlabel(xlabel if xlabel else (x if split is None else x))
    ax.set_ylabel(ylabel if ylabel else y)
    ax.set_title(title)

    return fig, ax


# =============================================================================
# Helper Functions
# =============================================================================

def _prepare_split_data(
    data: pd.DataFrame,
    x: str,
    y: str,
    split_col: str,
    split_order: Optional[List[str]] = None
) -> pd.DataFrame:
    """Prepare data for split bar plotting by creating a combined column."""
    data = data.copy()

    # If split_order is provided, ensure the split column follows that order
    if split_order is not None:
        data[split_col] = pd.Categorical(
            data[split_col], categories=split_order, ordered=True
        )
        data = data.sort_values([x, split_col])

    # Create a combined column that seaborn will use to separate bars
    data['_plot_group'] = data[x].astype(str) + '_' + data[split_col].astype(str)
    return data


def _create_default_hatch_mapping(split_values: Union[list, np.ndarray]) -> Dict[str, str]:
    """Create default hatch mapping for split values."""
    default_patterns = ['', '///', '\\\\\\', '|||', '---', '+++', 'xxx', '...']
    return {
        val: default_patterns[i % len(default_patterns)]
        for i, val in enumerate(split_values)
    }


def _apply_hatch_to_bars(
    ax: Axes,
    data: pd.DataFrame,
    split_col: str,
    hatch_mapping: Dict[str, str],
) -> None:
    """Apply hatch patterns to bars based on a split column."""
    # Get split values in the order specified by hatch_mapping
    split_values = list(hatch_mapping.keys())
    n_splits = len(split_values)

    for idx, patch in enumerate(ax.patches):
        if hasattr(patch, 'get_height'):  # Check if it's a bar
            split_idx = idx % n_splits
            split_val = split_values[split_idx]
            patch.set_hatch(hatch_mapping[split_val])


def _fix_split_xticks(
    ax: Axes,
    plot_data: pd.DataFrame,
    original_data: pd.DataFrame,
    x: str,
    split: str
) -> None:
    """Fix x-axis tick labels for split bar plots."""
    # Get unique x categories in order
    x_labels = []
    seen = set()
    for label in plot_data['_plot_group']:
        main_label = label.split('_')[0]
        if main_label not in seen:
            x_labels.append(main_label)
            seen.add(main_label)

    # Calculate tick positions (center of each group)
    n_splits = len(original_data[split].unique())
    tick_positions = []
    for i, label in enumerate(x_labels):
        # Calculate center position for each group
        center = (n_splits * i) + (n_splits - 1) / 2
        tick_positions.append(center)

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(x_labels)
