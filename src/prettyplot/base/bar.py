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

    # Apply orders if specified
    if order is not None:
        plot_data[x] = pd.Categorical(plot_data[x], categories=order, ordered=True)
    if hatch is not None and hatch_order is not None:
        plot_data[hatch] = pd.Categorical(plot_data[hatch], categories=hatch_order, ordered=True)

    # Create hatch_mapping if hatch is provided
    if hatch is not None and hatch_mapping is None:
        hatch_values = plot_data[hatch].unique()
        hatch_mapping = _create_default_hatch_mapping(hatch_values)

    # Determine the strategy for handling hatch and hue
    # Key insight: use hue=hatch for splitting when needed, then override colors

    needs_hatch_splitting = False
    needs_color_override = False
    override_color = None
    seaborn_hue = None
    hue_order_for_patches = None

    if hatch is not None:
        # Check if hatch is the categorical variable (x or y)
        hatch_is_categorical = (hatch == x)

        if not hatch_is_categorical:
            # hatch != x|y: need to split by hatch for proper placement
            needs_hatch_splitting = True
            seaborn_hue = hatch
            hue_order_for_patches = sorted(plot_data[hatch].unique())

            if hue is None:
                # No hue: use single color for all bars
                needs_color_override = True
                override_color = color if color is not None else DEFAULT_COLOR
            elif hue == x:
                # hue is the categorical variable: override to x-based colors
                needs_color_override = True
                override_color = None  # Will use palette
            elif hue == hatch:
                # hue == hatch: no override needed, colors are correct
                needs_color_override = False
            else:
                # hue != hatch != x|y: sophisticated case
                # Create combined grouping
                plot_data['_combined_group'] = (
                    plot_data[hue].astype(str) + '_' + plot_data[hatch].astype(str)
                )
                seaborn_hue = '_combined_group'
                hue_order_for_patches = sorted(plot_data['_combined_group'].unique())
                needs_color_override = True  # Will override to hue-based colors
                override_color = None  # Will use palette
        else:
            # hatch == x|y: just apply hatches, use standard hue behavior
            seaborn_hue = hue if hue is not None else x
            hue_order_for_patches = sorted(plot_data[seaborn_hue].unique())
            needs_hatch_splitting = False
    else:
        # No hatch: standard behavior
        seaborn_hue = hue
        if hue is not None:
            hue_order_for_patches = sorted(plot_data[hue].unique())

    # Build seaborn palette
    if seaborn_hue is not None:
        if needs_hatch_splitting and not needs_color_override:
            # hue == hatch: use resolved_palette directly
            seaborn_palette = resolved_palette
        elif needs_hatch_splitting and needs_color_override:
            # Will override colors: don't pass palette to seaborn or use dummy
            seaborn_palette = None
        elif needs_hatch_splitting and hue is not None and hue != hatch and hue != x:
            # Sophisticated case: palette maps combined groups to hue colors
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
        else:
            # Standard case
            seaborn_palette = resolved_palette if resolved_palette is not None else None
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
    if seaborn_hue is not None:
        barplot_kwargs['hue'] = seaborn_hue
        if seaborn_palette is not None:
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

    # Apply hatch patterns and override colors if needed
    if hatch is not None:
        _apply_hatches_and_override_colors(
            ax=ax,
            data=data,
            x_col=x,
            hue_col=hue,
            hatch_col=hatch,
            hue_order_for_patches=hue_order_for_patches,
            hatch_mapping=hatch_mapping,
            needs_color_override=needs_color_override,
            override_color=override_color,
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


def _apply_hatches_and_override_colors(
    ax: Axes,
    data: pd.DataFrame,
    x_col: str,
    hue_col: Optional[str],
    hatch_col: str,
    hue_order_for_patches: List[str],
    hatch_mapping: Dict[str, str],
    needs_color_override: bool,
    override_color: Optional[str],
    color_palette: Union[Dict, List],
    alpha: float,
) -> None:
    """
    Apply hatch patterns using patch.get_label() trick and override colors if needed.

    Strategy:
    1. Use idx // n_x to determine which hue group each patch belongs to
    2. Apply hatch pattern based on hatch_col value
    3. If needs_color_override, override colors based on hue_col or x_col
    """
    n_x = data[x_col].nunique()
    n_hue = len(hue_order_for_patches)
    total_bars = n_x * n_hue

    for idx, patch in enumerate(ax.patches):
        if not hasattr(patch, 'get_height'):
            continue

        # Determine which layer (outline=0, fill=1)
        layer = idx // total_bars
        # Position within layer
        bar_idx = idx % total_bars

        # Get the hue category for this bar using idx // n_x approach
        hue_idx = bar_idx % n_hue
        hue_val = hue_order_for_patches[hue_idx]

        # Get x category for this bar
        x_idx = bar_idx // n_hue
        x_vals = sorted(data[x_col].unique())
        x_val = x_vals[x_idx]

        # Determine hatch value
        if hue_col is not None and hue_col != hatch_col and '_combined_group' not in hue_order_for_patches[0]:
            # hue != hatch, not combined: hue_val is from hatch_col
            hatch_val = hue_val
        elif '_' in str(hue_val) and hue_col is not None and hue_col != hatch_col:
            # Combined group: parse to get hatch value
            parts = str(hue_val).split('_', 1)
            hatch_val = parts[1] if len(parts) == 2 else hue_val
        else:
            # hue == hatch or only hatch or only hue
            hatch_val = hue_val

        # Apply hatch pattern
        hatch_pattern = hatch_mapping.get(hatch_val, '')
        patch.set_hatch(hatch_pattern)

        # Override color if needed
        if needs_color_override:
            if override_color is not None:
                # Single color for all bars
                color = override_color
            elif hue_col is not None:
                if '_' in str(hue_val) and hue_col != hatch_col:
                    # Combined group: parse to get hue value for coloring
                    parts = str(hue_val).split('_', 1)
                    color_val = parts[0] if len(parts) == 2 else hue_val
                elif hue_col == x_col:
                    # hue is x: use x value for coloring
                    color_val = x_val
                else:
                    color_val = hue_val

                # Get color from palette
                if isinstance(color_palette, dict):
                    color = color_palette.get(color_val, 'black')
                elif isinstance(color_palette, list):
                    # Find index of color_val in sorted hue values
                    if hue_col == x_col:
                        vals = x_vals
                        val_idx = x_idx
                    else:
                        vals = sorted(data[hue_col].unique())
                        val_idx = vals.index(color_val) if color_val in vals else 0
                    color = color_palette[val_idx % len(color_palette)]
                else:
                    color = 'black'
            else:
                # Should not happen, but fallback
                color = 'black'

            # Apply color
            if layer == 0:  # Outline layer
                patch.set_edgecolor(color)
            else:  # Fill layer
                patch.set_facecolor(color)


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
