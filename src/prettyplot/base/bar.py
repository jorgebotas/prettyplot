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
    user_color_palette = None  # Store user's desired color scheme

    # Determine if we need to use color or palette
    has_grouping = hue is not None or hatch is not None

    if has_grouping:
        # When there's grouping (hue or hatch), use palette
        if isinstance(palette, str) or palette is None:
            # Determine number of colors needed based on actual coloring column
            if hatch is not None and hue is not None:
                # Both hatch and hue: color by hue, group by hatch
                n_colors = data[hue].nunique()
            elif hue is not None:
                # Only hue: standard behavior
                n_colors = data[hue].nunique()
            else:
                # Only hatch: color by x
                n_colors = data[x].nunique()
            resolved_palette = resolve_palette(palette, n_colors=n_colors)
        else:
            resolved_palette = palette

        # Store the user's color palette for later recoloring
        if hatch is not None:
            if hue is not None:
                # User wants to color by hue
                user_color_palette = resolved_palette
            else:
                # Color by x categories
                user_color_palette = resolved_palette

            # Create temporary palette for seaborn that maps hatch values
            # This is needed because we use hue=hatch for grouping
            resolved_palette = _create_hatch_palette(
                data, x, hatch, resolved_palette
            )
    else:
        # When there's no grouping, use custom color or default color
        bar_color = color if color is not None else DEFAULT_COLOR

    plot_data = data.copy()

    # Handle hatch bars (side-by-side grouped bars)
    if hatch is not None:
        # Apply hatch_order if specified
        if hatch_order is not None:
            plot_data[hatch] = pd.Categorical(
                plot_data[hatch], categories=hatch_order, ordered=True
            )

        # Create default hatch mapping if not provided
        if hatch_mapping is None:
            hatch_values = plot_data[hatch].unique()
            hatch_mapping = _create_default_hatch_mapping(hatch_values)

        # Use seaborn's native hue-based grouping for better bar positioning
        plot_x = x
        plot_hue_col = hatch
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

    # Apply hatch patterns and recolor bars if hatch is used
    if hatch is not None:
        # Determine the coloring column and prepare palette
        if hue is not None:
            color_col = hue
        else:
            color_col = x

        # Convert user_color_palette to dict if it's a list
        if isinstance(user_color_palette, list):
            color_values = sorted(data[color_col].unique())
            color_palette_dict = {
                val: user_color_palette[i % len(user_color_palette)]
                for i, val in enumerate(color_values)
            }
        else:
            color_palette_dict = user_color_palette

        # First, recolor bars based on the desired coloring scheme
        _recolor_bars_by_category(
            ax=ax,
            data=data,
            x_col=x,
            hatch_col=hatch,
            color_col=color_col,
            palette=color_palette_dict,
            alpha=alpha
        )

        # Then apply hatch patterns
        _apply_hatch_to_bars(
            ax=ax,
            data=data,
            x_col=x,
            hatch_col=hatch,
            hatch_mapping=hatch_mapping,
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


def _create_hatch_palette(
    data: pd.DataFrame,
    x_col: str,
    hatch_col: str,
    x_palette: Union[List, Dict]
) -> Dict:
    """
    Create a palette for hatch-based plotting that colors by x categories.

    When using hue=hatch for grouping, we need to map hatch values to colors
    based on their corresponding x categories. Since each hatch value appears
    across multiple x categories, we create a simple palette that cycles through
    x colors for each hatch value.
    """
    # For simplicity, just create a palette that maps hatch values to colors
    # We'll recolor bars manually after plotting
    hatch_values = data[hatch_col].unique()
    if isinstance(x_palette, dict):
        colors = list(x_palette.values())
    else:
        colors = list(x_palette)

    # Return a simple mapping - we'll fix colors later
    return {hatch_val: colors[i % len(colors)] for i, hatch_val in enumerate(hatch_values)}


def _recolor_bars_by_category(
    ax: Axes,
    data: pd.DataFrame,
    x_col: str,
    hatch_col: str,
    color_col: str,
    palette: Dict,
    alpha: float
) -> None:
    """
    Recolor bars to match a specific category instead of hatch categories.

    When using hue=hatch for grouping, seaborn colors by hatch values.
    This function recolors bars based on a specified color column.

    Parameters
    ----------
    color_col : str
        Column to use for coloring (e.g., x_col or a separate hue column)
    """
    x_values = sorted(data[x_col].unique())
    hatch_values = list(data[hatch_col].unique())
    n_hatch = len(hatch_values)
    n_x = len(x_values)

    # Create a mapping from (x_value, hatch_value) to color_value
    color_map = {}
    for _, row in data.iterrows():
        key = (row[x_col], row[hatch_col])
        color_map[key] = row[color_col]

    # Total number of bars in each layer (outline and fill)
    total_bars = n_x * n_hatch
    n_patches = len(ax.patches)
    n_layers = n_patches // total_bars if total_bars > 0 else 1

    # Recolor all patches
    for idx, patch in enumerate(ax.patches):
        if hasattr(patch, 'get_height'):  # Check if it's a bar
            # Determine which (x, hatch) combination this bar belongs to
            bar_idx = idx % total_bars
            x_idx = bar_idx // n_hatch
            hatch_idx = bar_idx % n_hatch
            x_val = x_values[x_idx]
            hatch_val = hatch_values[hatch_idx]

            # Get the color value for this (x, hatch) combination
            color_val = color_map.get((x_val, hatch_val))
            if color_val is not None:
                color = palette.get(color_val, 'black')
            else:
                color = 'black'

            # Set color based on layer (outline vs fill)
            layer = idx // total_bars
            if layer == 0:  # First layer (outline)
                patch.set_edgecolor(color)
            else:  # Second layer (fill)
                patch.set_facecolor(color)


def _apply_hatch_to_bars(
    ax: Axes,
    data: pd.DataFrame,
    x_col: str,
    hatch_col: str,
    hatch_mapping: Dict[str, str],
) -> None:
    """Apply hatch patterns to grouped bars based on hatch column."""
    # Get hatch values in the order they appear
    hatch_values = list(hatch_mapping.keys())
    n_hatch = len(hatch_values)
    n_x = data[x_col].nunique()

    # Apply hatch patterns to all patches
    # When using seaborn with hue, patches are organized as:
    # [x1_hatch1, x1_hatch2, ..., x2_hatch1, x2_hatch2, ...]
    for idx, patch in enumerate(ax.patches):
        if hasattr(patch, 'get_height'):  # Check if it's a bar
            # Determine which hatch value this patch corresponds to
            bar_idx = idx % (n_x * n_hatch)
            hatch_idx = bar_idx % n_hatch
            hatch_val = hatch_values[hatch_idx]
            patch.set_hatch(hatch_mapping[hatch_val])


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
