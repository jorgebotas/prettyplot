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
    hatch: Optional[str] = None,
    color: Optional[str] = None,
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
    hatch_order: Optional[List[str]] = None,
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
        Column name for color grouping (typically same as x for hatched bars).
    hatch : str, optional
        Column name for splitting bars side-by-side with hatch patterns.
        When specified, creates grouped bars within each x category.
    color : str, optional
        Fixed color for all bars (only used when hue is None).
        Overrides DEFAULT_COLOR. Example: '#ff0000' or 'red'.
    ax : Axes, optional
        Matplotlib axes object. If None, creates new figure.
    title : str, default=""
        Plot title.
    xlabel : str, default=""
        X-axis label. If empty and hatch is used, uses x column name.
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
        Mapping from hatch values to hatch patterns.
        Example: {'group1': '', 'group2': '///', 'group3': '\\\\\\'}
    errorbar : str, default='se'
        Error bar type: 'se' (standard error), 'sd' (standard deviation),
        'ci' (confidence interval), or None for no error bars.
    gap : float, default=0.1
        Gap between bar groups (0-1).
    order : list, optional
        Order of x-axis categories.
    hatch_order : list, optional
        Order of hatch categories. If provided, determines bar order within groups.
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

    Bar plot with hatched bars and patterns:
    >>> fig, ax = pp.barplot(
    ...     data=df, x='condition', y='measurement',
    ...     hatch='treatment', hue='condition',
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
    has_grouping = hue is not None or hatch is not None

    if has_grouping:
        # When there's grouping (hue or hatch), use palette
        if isinstance(palette, str) or palette is None:
            # Determine number of colors needed
            if hue is not None:
                # User provided explicit hue - use that for coloring
                n_colors = data[hue].nunique()
            elif hatch is not None:
                # Hatch provided without hue - color by x categories
                n_colors = data[x].nunique()
            else:
                n_colors = data[x].nunique()
            resolved_palette = resolve_palette(palette, n_colors=n_colors)
        else:
            resolved_palette = palette
    else:
        # When there's no grouping, use custom color or default color
        bar_color = color if color is not None else DEFAULT_COLOR

    plot_data = data.copy()

    # Handle hatch bars (side-by-side grouped bars)
    if hatch is not None:
        # Get hatch order from hatch_mapping keys if provided, otherwise from data
        if hatch_order is not None:
            split_order = hatch_order
        elif hatch_mapping is not None:
            split_order = list(hatch_mapping.keys())
        else:
            split_order = None

        # Prepare split data with _plot_group column
        plot_data = _prepare_split_data(
            plot_data, x, y, hatch, split_order=split_order
        )
        plot_x = '_plot_group'

        # When hatch is used, we color by x (or by hue if provided)
        # This ensures bars are colored by their x category (or hue category)
        if hue is not None:
            plot_hue_col = hue
        else:
            plot_hue_col = x

        # Create default hatch mapping if not provided
        if hatch_mapping is None:
            hatch_values = data[hatch].unique()
            hatch_mapping = _create_default_hatch_mapping(hatch_values)
    else:
        plot_x = x
        plot_hue_col = hue

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

    # Add hue for grouping if needed
    if plot_hue_col is not None:
        barplot_kwargs['hue'] = plot_hue_col

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

    # Apply hatch patterns if hatch is used
    if hatch is not None:
        _apply_hatch_to_bars(
            ax=ax,
            data=data,
            split_col=hatch,
            hatch_mapping=hatch_mapping,
        )

        # Clean up x-axis labels to show only main categories
        _fix_split_xticks(ax, plot_data, data, x, hatch)

    # Add legend if hue or hatch is used
    if hue is not None or hatch is not None:
        _create_barplot_legend(
            ax=ax,
            data=data,
            hue=hue,
            hatch=hatch,
            palette=resolved_palette,
            hatch_mapping=hatch_mapping,
            alpha=alpha,
            linewidth=linewidth
        )

    # Set labels
    ax.set_xlabel(xlabel if xlabel else (x if hatch is None else x))
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
    """
    Apply hatch patterns to bars based on a split column.

    Matches the logic from the original example: simply cycles through
    hatch patterns based on bar index modulo number of split values.
    """
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


def _create_barplot_legend(
    ax: Axes,
    data: pd.DataFrame,
    hue: Optional[str],
    hatch: Optional[str],
    palette: Optional[Union[str, Dict, List]],
    hatch_mapping: Optional[Dict[str, str]],
    alpha: float,
    linewidth: float
) -> None:
    """
    Create a combined legend for barplot with doublemarker trick.

    This function creates legend entries that properly represent both the filled
    (with alpha) and outlined bars, avoiding duplicate legend entries.
    """
    import matplotlib.patches as mpatches

    # Determine what to show in legend
    if hatch is not None:
        # For hatched bars, create legend entries for each hatch category
        legend_labels = list(hatch_mapping.keys())
        legend_handles = []

        # Get one representative color for the legend (use first color from palette)
        # All hatch patterns will use the same color in the legend
        if isinstance(palette, dict):
            sample_color = list(palette.values())[0] if palette else 'black'
        elif isinstance(palette, list):
            sample_color = palette[0] if palette else 'black'
        else:
            sample_color = 'black'

        # Create custom legend handles with fill + edge + hatch
        for label in legend_labels:
            hatch_pattern = hatch_mapping[label]
            handle = mpatches.Patch(
                facecolor=sample_color,
                edgecolor=sample_color,
                alpha=alpha,
                linewidth=linewidth,
                hatch=hatch_pattern,
                label=label
            )
            legend_handles.append(handle)

        ax.legend(
            handles=legend_handles,
            labels=legend_labels,
            bbox_to_anchor=(1, 1),
            loc='upper left',
            frameon=False
        )

    elif hue is not None:
        # For hue-based bars, create legend entries for each hue category
        hue_values = sorted(data[hue].unique())
        legend_handles = []

        # Map hue values to colors
        if isinstance(palette, dict):
            colors = [palette.get(val, 'black') for val in hue_values]
        elif isinstance(palette, list):
            colors = palette[:len(hue_values)]
        else:
            colors = ['black'] * len(hue_values)

        # Create custom legend handles with fill + edge
        for i, label in enumerate(hue_values):
            color = colors[i] if i < len(colors) else 'black'
            handle = mpatches.Patch(
                facecolor=color,
                edgecolor=color,
                alpha=alpha,
                linewidth=linewidth,
                label=str(label)
            )
            legend_handles.append(handle)

        ax.legend(
            handles=legend_handles,
            labels=[str(val) for val in hue_values],
            bbox_to_anchor=(1, 1),
            loc='upper left',
            frameon=False
        )
