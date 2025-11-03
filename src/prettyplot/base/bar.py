"""
Bar plot functions for prettyplot.

This module provides publication-ready bar plot visualizations with
flexible styling and grouping options.
"""

from typing import Optional, List, Dict, Tuple, Union
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
import seaborn as sns
import pandas as pd
import numpy as np

from prettyplot.config import DEFAULT_LINEWIDTH, DEFAULT_ALPHA, DEFAULT_CAPSIZE, DEFAULT_FIGSIZE
from prettyplot.themes.colors import resolve_palette_mapping, DEFAULT_COLOR
from prettyplot.themes.hatches import resolve_hatch_mapping
from prettyplot.utils import is_categorical

_SPLIT_SEPARATOR = "---"

def barplot(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: Optional[str] = None,
    hatch: Optional[str] = None,
    color: Optional[str] = DEFAULT_COLOR,
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
    legend: bool = True,
    errorbar: str = "se",
    gap: float = 0.1,
    hue_order: Optional[List[str]] = None,
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
        Overrides DEFAULT_COLOR. Example: "#ff0000" or "red".
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
        Example: {"group1": "", "group2": "///", "group3": "\\\\\\"}
    legend : bool, default=True
        Whether to show the legend.
    errorbar : str, default="se"
        Error bar type: "se" (standard error), "sd" (standard deviation),
        "ci" (confidence interval), or None for no error bars.
    gap : float, default=0.1
        Gap between bar groups (0-1).
    hue_order : list, optional
        Hue order. If provided, determines bar order within groups.
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
    >>> fig, ax = pp.barplot(data=df, x="category", y="value")

    Bar plot with color groups:
    >>> fig, ax = pp.barplot(data=df, x="category", y="value",
    ...                       hue="group", palette="pastel_categorical")

    Bar plot with hatched bars and patterns:
    >>> fig, ax = pp.barplot(
    ...     data=df, x="condition", y="measurement",
    ...     hatch="treatment", hue="condition",
    ...     hatch_mapping={"control": "", "treated": "///"},
    ...     palette={"A": "#75b375", "B": "#8e8ec1"}
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


    # Get hue palette and hatch mappings
    palette = resolve_palette_mapping(
        values=data[hue].unique() if hue is not None else None,
        palette=palette,
    )
    hatch_mapping = resolve_hatch_mapping(
        values=data[hatch].unique() if hatch is not None else None,
        hatch_mapping=hatch_mapping,
    )

    data = _prepare_split_data(
        data, 
        hue, 
        hatch, 
        orderA=hue_order or list(palette.keys()) if hue is not None else None, 
        orderB=hatch_order or list(hatch_mapping.keys()) if hatch is not None else None
    )

    # Determine the strategy for handling hatch and hue
    # Key insight: use hue=hatch for splitting when needed, then override colors
    sns_hue = hue
    sns_palette = palette

    # Fint out categorical axis
    categorical_axis = x if is_categorical(data[x]) else y

    # hatch split only needed if hatch is not the same as the categorical axis
    split_by_hatch = hatch is not None and hatch != categorical_axis
    double_split = split_by_hatch and hue is not None and hue != categorical_axis and hatch != hue
    if split_by_hatch:
        if double_split:
            # Need to create double split by creating a new column with the combined value of hue and hatch
            sns_hue = f"{hue}_{hatch}"
            # Color bars by 
            sns_palette = {
                x: palette[x.split(_SPLIT_SEPARATOR)[0]] for x in data[f"{hue}_{hatch}"].cat.categories
            }
        else:
            # Only need to split by hatch
            # We will recolor the bars to color argument if hue is None
            sns_hue = hatch
            sns_palette = None

    # Prepare kwargs for seaborn barplot
    barplot_kwargs = {
        "data": data,
        "x": x,
        "y": y,
        "hue": sns_hue,
        "palette": sns_palette if sns_hue else None,
        "color": color,
        "fill": False,
        "linewidth": linewidth,
        "capsize": capsize,
        "ax": ax,
        "err_kws": {"linewidth": linewidth},
        "errorbar": errorbar,
        "gap": gap,
        "legend": False,
    }

    # Merge with user-provided kwargs
    barplot_kwargs.update(kwargs)

    # Create outline bars
    sns.barplot(**barplot_kwargs)

    # Add filled bars with alpha if needed
    if 0 < alpha <= 1:
        fill_kwargs = barplot_kwargs.copy()
        fill_kwargs.update({
            "fill": True,
            "alpha": alpha,
            "linewidth": 0,
            "errorbar": None,
            "err_kws": {"linewidth": 0},
        })
        sns.barplot(**fill_kwargs)

    # Apply hatch patterns and override colors if needed
    if hatch is not None:
        _apply_hatches_and_override_colors(
            ax=ax,
            data=data,
            hue=hue,
            hatch=hatch,
            categorical_axis=categorical_axis,
            double_split=double_split,
            linewidth=linewidth,
            color=color,
            palette=palette,
            hatch_mapping=hatch_mapping,
        )

    # Add legend if hue or hatch is used
    # if legend:
    #     _create_barplot_legend(
    #         ax=ax,
    #         data=data,
    #         hue=hue,
    #         hatch=hatch,
    #         palette=palette,
    #         hatch_mapping=hatch_mapping,
    #         alpha=alpha,
    #         linewidth=linewidth
    #     )

    # Set labels
    if xlabel is not None: ax.set_xlabel(xlabel)
    if ylabel is not None: ax.set_ylabel(ylabel)
    if title is not None: ax.set_title(title)

    return fig, ax


# =============================================================================
# Helper Functions
# =============================================================================


def _prepare_split_data(
        data: pd.DataFrame, 
        colA: str,
        colB: str,
        orderA: Optional[List[str]] = None,
        orderB: Optional[List[str]] = None,
    ) -> pd.DataFrame:
    """
    Prepare data for split bar plotting by creating a combined column.
    
    Parameters
    ----------
    data : DataFrame
        Input data
    colA : str
        Column name for first split
    colB : str
        Column name for second split
    orderA : list, optional
        Order of column A values. If provided, data will be sorted to match this order.
    orderB : list, optional
        Order of column B values. If provided, data will be sorted to match this order.
    
    Returns
    -------
    DataFrame
        Data with new combined column for proper bar separation and sorted by the order of the columns
        New column name is f"{colA}_{colB}"
    """
    data = data.copy()
    
    # If order is provided, ensure the split column follows that order
    prepareA = colA is not None and orderA is not None
    prepareB = colB is not None and orderB is not None
    if prepareA:
        data[colA] = pd.Categorical(data[colA], categories=orderA, ordered=True)
        data = data.sort_values([colA])
    if prepareB:
        data[colB] = pd.Categorical(data[colB], categories=orderB, ordered=True)
        data = data.sort_values([colB])

    # Sort the data by the columns in the order of the columns
    columns = ([colA] if prepareA else []) + ([colB] if prepareB else [])
    data.sort_values(columns, inplace=True)
    
    if prepareA and prepareB:
        # Create a combined column that seaborn will use to separate bars
        data[f"{colA}_{colB}"] = data[colA].astype(str) + _SPLIT_SEPARATOR + data[colB].astype(str)
        data[f"{colA}_{colB}"] = pd.Categorical(
            data[f"{colA}_{colB}"],
            categories=data[f"{colA}_{colB}"].unique(),
            ordered=True
        )
    return data

def _apply_hatches_and_override_colors(
        ax: Axes,
        data: pd.DataFrame,
        hue: Optional[str],
        hatch: str,
        categorical_axis: str,
        double_split: bool,
        linewidth: float,
        color: Optional[str],
        palette: Optional[Union[str, Dict, List]],
        hatch_mapping: Optional[Dict[str, str]],
    ) -> None:
    """
    Apply hatch patterns using patch.get_label() and idx // n_x, then override colors.

    Uses the approach from user"s example:
    - Track which category each patch belongs to via idx // n_x
    - Use patch.get_label() or hue_order to determine the category
    - Apply hatch based on the hatch column value
    - Override colors if needed
    """
    # Override color if hue is not defined (default to color argument)
    # Or if hue is not the same as hatch
    override_color = hue is None or hue != hatch
    n_axis = len(data[categorical_axis].unique())
    n_hue = len(data[hue].unique()) if hue is not None else 1
    n_hatch = len(data[hatch].unique())  # always defined
    total_bars = n_axis * n_hue * n_hatch
    hue_order = list(palette.keys())
    hatch_order = list(hatch_mapping.keys())
    errorbars = ax.get_lines()

    for idx, patch in enumerate(ax.patches):
        if not hasattr(patch, "get_height"):
            continue

        bar_idx = idx % total_bars
        axis_idx = bar_idx % n_axis
        # Get hatch and hue index in palette and hatch_mapping
        # If hatch is the same as the categorical axis, we need to use the axis_idx
        hatch_idx = (bar_idx // n_axis) % n_hatch if hatch != categorical_axis else axis_idx
        # If double split, we take into account the combined index
        # Otherwise, if matching hatch and hue, we use the hatch index
        # Otherwise, we use the axis index
        hue_idx = (bar_idx // (n_axis * n_hatch)) if double_split else (
            hatch_idx if hue == hatch else axis_idx
        )

        # Determine which layer (outline -> alpha == 1, fill -> alpha < 1)
        alpha = patch.get_alpha()
        outline = alpha is None or (alpha == 1)
        if outline:
            # Apply hatch pattern
            hatch_pattern = hatch_mapping.get(hatch_order[hatch_idx], "")
            patch.set_hatch(hatch_pattern)
            patch.set_hatch_linewidth(linewidth)
        
        # Repaint the bars when needed
        color = palette[hue_order[hue_idx]] if hue is not None else color
        if not (double_split or hatch == categorical_axis):
            # Use the same color for all bars
            patch.set_edgecolor(color)
            if not outline: 
                patch.set_facecolor(color)
                patch.set_alpha(alpha)

            # Match error bar colors to bar colors
            # Only need to color the error bars 
            # for the outline bars (errorbar = None for fill bars)
            if bar_idx < len(errorbars):
                errorbars[bar_idx].set_color(color)