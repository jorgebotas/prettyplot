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
            # Determine number of colors needed based on what we're coloring by
            if hue is not None:
                n_colors = data[hue].nunique()
            elif hatch is not None:
                # When only hatch, color by x
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

    # Determine seaborn hue column for grouping
    # Key insight: hue and hatch should create same PLACEMENT, just different visual encoding
    if hue is not None and hatch is not None:
        if hue == hatch:
            # Same column for hue and hatch: group by that column, apply both color and hatch
            plot_hue_col = hue
            needs_combined_group = False
        else:
            # Different columns: create combined grouping
            plot_data['_combined_group'] = (
                plot_data[hue].astype(str) + '_' + plot_data[hatch].astype(str)
            )
            plot_hue_col = '_combined_group'
            needs_combined_group = True
    elif hue is not None:
        # Only hue: standard behavior
        plot_hue_col = hue
        needs_combined_group = False
    elif hatch is not None:
        # Only hatch: use hatch for grouping, but will recolor by x
        plot_hue_col = hatch
        needs_combined_group = False
    else:
        plot_hue_col = None
        needs_combined_group = False

    # Apply orders if specified
    if order is not None:
        plot_data[x] = pd.Categorical(plot_data[x], categories=order, ordered=True)
    if hatch is not None and hatch_order is not None:
        plot_data[hatch] = pd.Categorical(plot_data[hatch], categories=hatch_order, ordered=True)

    # Create hatch_mapping if hatch is provided
    if hatch is not None and hatch_mapping is None:
        hatch_values = plot_data[hatch].unique()
        hatch_mapping = _create_default_hatch_mapping(hatch_values)

    # Create the appropriate palette for seaborn
    if plot_hue_col is not None:
        if needs_combined_group:
            # Create palette mapping combined groups to colors based on hue column
            seaborn_palette = {}
            for _, row in plot_data[[hue, hatch, '_combined_group']].drop_duplicates().iterrows():
                combined_key = row['_combined_group']
                hue_val = row[hue]
                if isinstance(resolved_palette, dict):
                    seaborn_palette[combined_key] = resolved_palette.get(hue_val, 'black')
                elif isinstance(resolved_palette, list):
                    hue_vals = sorted(plot_data[hue].unique())
                    hue_idx = hue_vals.index(hue_val) if hue_val in hue_vals else 0
                    seaborn_palette[combined_key] = resolved_palette[hue_idx % len(resolved_palette)]
        elif hatch is not None and hue is None:
            # Only hatch: create palette mapping hatch values to x-based colors
            seaborn_palette = {}
            for _, row in plot_data[[x, hatch]].drop_duplicates().iterrows():
                hatch_val = row[hatch]
                x_val = row[x]
                if isinstance(resolved_palette, dict):
                    seaborn_palette[hatch_val] = resolved_palette.get(x_val, 'black')
                elif isinstance(resolved_palette, list):
                    x_vals = sorted(plot_data[x].unique())
                    x_idx = x_vals.index(x_val) if x_val in x_vals else 0
                    seaborn_palette[hatch_val] = resolved_palette[x_idx % len(resolved_palette)]
        else:
            # Standard hue or hue==hatch: use resolved_palette directly
            seaborn_palette = resolved_palette
    else:
        seaborn_palette = None

    # Prepare kwargs for seaborn barplot
    barplot_kwargs = {
        'data': plot_data,
        'x': x,
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
        barplot_kwargs['palette'] = seaborn_palette
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

    # Apply hatch patterns and fix colors if needed
    if hatch is not None:
        # Get hue order for tracking patches
        if plot_hue_col is not None:
            if needs_combined_group:
                hue_order = sorted(plot_data['_combined_group'].unique())
            else:
                hue_order = sorted(plot_data[plot_hue_col].unique())
        else:
            hue_order = None

        _apply_hatch_and_colors(
            ax=ax,
            data=data,
            x_col=x,
            hue_col=hue,
            hatch_col=hatch,
            hue_order=hue_order,
            hatch_mapping=hatch_mapping,
            needs_combined_group=needs_combined_group,
            color_palette=resolved_palette,
            alpha=alpha,
        )

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

def _create_default_hatch_mapping(split_values: Union[list, np.ndarray]) -> Dict[str, str]:
    """Create default hatch mapping for split values."""
    default_patterns = ['', '///', '\\\\\\', '|||', '---', '+++', 'xxx', '...']
    return {
        val: default_patterns[i % len(default_patterns)]
        for i, val in enumerate(split_values)
    }


def _apply_hatch_and_colors(
    ax: Axes,
    data: pd.DataFrame,
    x_col: str,
    hue_col: Optional[str],
    hatch_col: str,
    hue_order: List[str],
    hatch_mapping: Dict[str, str],
    needs_combined_group: bool,
    color_palette: Union[Dict, List],
    alpha: float,
) -> None:
    """
    Apply hatch patterns and fix colors using patch labels.

    Uses the approach from user's example: track which category each patch
    belongs to via idx // n_x_categories, then apply colors and hatches.
    """
    n_x = data[x_col].nunique()
    n_hue = len(hue_order)

    # Total patches per layer (outline and fill)
    total_bars = n_x * n_hue

    # Create mapping from hue_order value to (original_hue_val, hatch_val)
    if needs_combined_group:
        # Combined group: parse back to get original hue and hatch values
        category_map = {}
        for val in hue_order:
            parts = val.split('_', 1)
            if len(parts) == 2:
                category_map[val] = (parts[0], parts[1])
            else:
                category_map[val] = (val, val)
    elif hue_col is None:
        # Only hatch: need to determine x value for each bar to color correctly
        # Build mapping from hatch values to x values (for coloring)
        # Since each hatch appears at each x, we can't use a simple map
        # We'll handle this in the loop
        category_map = None
    else:
        # hue==hatch or only hue
        category_map = {val: (val, val) for val in hue_order}

    for idx, patch in enumerate(ax.patches):
        if not hasattr(patch, 'get_height'):
            continue

        # Determine which layer (outline=0, fill=1)
        layer = idx // total_bars
        # Position within layer
        bar_idx = idx % total_bars

        # Get the hue category for this bar using the user's approach
        hue_idx = bar_idx % n_hue
        hue_val = hue_order[hue_idx]

        # Get x category for this bar
        x_idx = bar_idx // n_hue
        x_vals = sorted(data[x_col].unique())
        x_val = x_vals[x_idx]

        # Determine color and hatch based on scenario
        if needs_combined_group:
            # hue and hatch are different columns
            orig_hue_val, hatch_val = category_map[hue_val]
            # Color by original hue value
            if isinstance(color_palette, dict):
                color = color_palette.get(orig_hue_val, 'black')
            elif isinstance(color_palette, list):
                hue_vals = sorted(data[hue_col].unique())
                hue_palette_idx = hue_vals.index(orig_hue_val) if orig_hue_val in hue_vals else 0
                color = color_palette[hue_palette_idx % len(color_palette)]
            else:
                color = 'black'
        elif hue_col is None:
            # Only hatch: color by x value
            if isinstance(color_palette, dict):
                color = color_palette.get(x_val, 'black')
            elif isinstance(color_palette, list):
                color = color_palette[x_idx % len(color_palette)]
            else:
                color = 'black'
            hatch_val = hue_val  # hue_order contains hatch values
        else:
            # hue==hatch or only hue
            color = None  # Keep seaborn's color
            hatch_val = hue_val

        # Apply color if needed (only hatch or combined group)
        if color is not None:
            if layer == 0:  # Outline layer
                patch.set_edgecolor(color)
            else:  # Fill layer
                patch.set_facecolor(color)

        # Apply hatch pattern
        hatch_pattern = hatch_mapping.get(hatch_val, '')
        patch.set_hatch(hatch_pattern)


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
