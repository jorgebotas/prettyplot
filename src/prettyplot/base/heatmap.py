"""
Circle Heatmap Visualization Module

Provides flexible scatter-based heatmap visualizations with distinctive 
double-layer markers (transparent fill + solid borders) for enhanced visibility.
Supports both categorical and continuous color mapping.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Circle
from matplotlib.legend_handler import HandlerBase
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize, ListedColormap
import pandas as pd
import numpy as np
from typing import Optional, Tuple, Union, Dict, List

plt.rcParams["pdf.fonttype"] = 42
sns.set_theme("paper", style="white", font="Arial", font_scale=1.6)


# ============================================================================
# Legend Handlers
# ============================================================================

DEFAULT_CBAR_KWS = dict(
    shrink=0.3, 
    aspect=5, 
    location="right", 
    pad=0.1, 
    anchor=(0.5, 1) # Anchor to top center
)
DEFAULT_GRID_KWS = dict(
    alpha=0.2,
    linestyle="--",
    linewidth=0.5,
    zorder=1
)


from matplotlib.legend_handler import HandlerBase
class HandlerCircle(HandlerBase):
    """
    Custom legend handler for double-layer circle markers.
    
    Creates markers with transparent fill and solid borders for use in legends,
    maintaining consistency with the main plot style.
    
    Parameters
    ----------
    alpha : float, default=0.1
        Transparency level for the fill layer.
    linewidth : float, default=2
        Width of the edge circle.
    """
    
    def __init__(self, alpha: float = 0.1, linewidth: float = 2, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.linewidth = linewidth
    
    def create_artists(
        self,
        legend,
        orig_handle,
        xdescent,
        ydescent,
        width,
        height,
        fontsize,
        trans
    ) -> List[Circle]:
        """Create the legend marker artists."""
        # Center point
        cx = 0.5 * width - 0.5 * xdescent
        cy = 0.5 * height - 0.5 * ydescent
        
        # Extract properties from the handle
        if isinstance(orig_handle, tuple):
            color, size = orig_handle
        else:
            color = (
                orig_handle.get_color() 
                if hasattr(orig_handle, "get_color") 
                else "gray"
            )
            size = (
                orig_handle.get_markersize() 
                if hasattr(orig_handle, "get_markersize") 
                else DEFAULT_MARKER_SIZE
            )
        
        # Create filled circle with transparency
        circle_fill = Circle(
            (cx, cy),
            size / 2,
            color=color,
            alpha=self.alpha,
            transform=trans,
            linewidth=0
        )
        
        # Create edge circle
        circle_edge = Circle(
            (cx, cy),
            size / 2,
            facecolor="none",
            edgecolor=color,
            linewidth=self.linewidth,
            transform=trans
        )
        
        return [circle_fill, circle_edge]


# ============================================================================
# Core Plotting Functions
# ============================================================================

def scatterplot_double_markers(
    data: pd.DataFrame,
    x: str,
    y: str,
    size: str,
    hue: str,
    palette: Optional[Union[str, Dict, List]] = None,
    hue_norm: Optional[Normalize] = None,
    sizes: Tuple[float, float] = (50, 1000),
    alpha: float = 0.1,
    linewidth: float = 2,
    edgecolor: Optional[str] = None,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Create a scatter plot with double-layer markers (transparent fill + solid edge).
    
    Uses two overlaid seaborn scatterplots to achieve the distinctive visual effect
    of transparent filled circles with crisp solid borders. This cannot be achieved
    with a single matplotlib marker as marker properties are uniform.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    x : str
        Column name for x-axis positions.
    y : str
        Column name for y-axis positions.
    size : str
        Column name for marker sizes.
    hue : str
        Column name for marker colors.
    palette : str, dict, list, or None
        Color palette. Can be a seaborn palette name, dict mapping hue values
        to colors, or list of colors. If None, uses default seaborn palette.
    hue_norm : Normalize, optional
        Normalization for continuous hue values. If provided, enables continuous
        color mapping.
    sizes : tuple of float, default=(50, 1000)
        Min and max marker sizes in points^2.
    alpha : float, default=0.1
        Transparency level for the fill layer.
    linewidth : float, default=2
        Width of the edge circles.
    edgecolor : str, defaul=None
        Optional edge color. If None, the edge color is the same as the fill color.
    ax : plt.Axes, optional
        Matplotlib axes object. If None, creates new figure.
    
    Returns
    -------
    ax : plt.Axes
        The matplotlib axes object containing the plot.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 4))
    
    # Layer 1: Filled circles with transparency
    sns.scatterplot(
        data=data,
        x=x,
        y=y,
        size=size,
        hue=hue,
        palette=palette,
        hue_norm=hue_norm,
        sizes=sizes,
        alpha=alpha,
        edgecolor="none",
        linewidth=0,
        ax=ax,
        legend=False,
        zorder=2,
    )
    
    # Layer 2: Edge-only circles for crisp borders
    sns.scatterplot(
        data=data,
        x=x,
        y=y,
        size=size,
        hue=hue,
        palette=palette,
        hue_norm=hue_norm,
        sizes=sizes,
        alpha=1.0,
        linewidth=linewidth,
        ax=ax,
        legend=False,
        zorder=3,
    )
    
    # Modify the second layer to be hollow
    collections = ax.collections
    if len(collections) >= 2:
        edge_collection = collections[-1]
        face_collection = collections[-2]
        
        # Make hollow: no fill, but use fill colors as edge colors
        edge_collection.set_facecolors("none")
        edge_collection.set_edgecolors(edgecolor or face_collection.get_facecolors())
        edge_collection.set_linewidths(linewidth)
    
    return ax


def circle_heatmap(
    data: pd.DataFrame,
    x: str,
    y: str,
    size: str,
    hue: str,
    palette: Optional[Union[str, Dict, List]] = None,
    hue_order: Optional[List] = None,
    x_order: Optional[List] = None,
    y_order: Optional[List] = None,
    sizes: Tuple[float, float] = (50, 900),
    size_norm: Optional[Tuple[float, float]] = None,
    hue_norm: Optional[Tuple[float, float]] = None,
    alpha: float = 0.1,
    linewidth: float = 2,
    edgecolor: Optional[str] = None,
    figsize: Optional[Tuple[float, float]] = None,
    figsize_factors: Tuple[float, float] = (2, 2/3),
    ax: Optional[plt.Axes] = None,
    cbar: bool = True,
    size_legend: bool = True,
    size_legend_title: Optional[str] = None,
    hue_legend: bool = True,
    hue_legend_title: Optional[str] = None,
    cbar_kws: Optional[Dict] = None,
    hue_legend_kws: Optional[Dict] = None,
    size_legend_kws: Optional[Dict] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    sort_x: bool = True,
    sort_y: bool = True,
    invert_y: bool = True,
    grid: bool = False,
    grid_kws: Optional[Dict] = None,
    xticks_kws: Optional[Dict] = None,
    yticks_kws: Optional[Dict] = None,
) -> Tuple[plt.Axes, Optional[ColorbarBase]]:
    """
    Create a circle-based heatmap with flexible categorical or continuous coloring.
    
    This function creates scatter-based heatmaps with distinctive double-layer
    markers (transparent fill + solid borders) arranged in a grid. Supports both
    categorical colors (with legend) and continuous colors (with colorbar).
    
    Parameters
    ----------
    data : pd.DataFrame
        Input data containing x, y, size, and hue columns.
    x : str
        Column name for x-axis categories/positions.
    y : str
        Column name for y-axis categories/positions.
    size : str
        Column name for marker sizes. Values are mapped to circle areas.
    hue : str
        Column name for marker colors. Can be categorical or continuous.
    palette : str, dict, list, or None
        Color specification:
        - str: seaborn palette name (e.g., "viridis", "Set2")
        - dict: mapping of hue values to colors (for categorical)
        - list: list of colors (for categorical)
        - None: uses default seaborn palette
    hue_order : list, optional
        Order for categorical hue values. If None, sorted automatically.
    x_order : list, optional
        Order for x-axis categories. If None, uses sort_x parameter.
    y_order : list, optional
        Order for y-axis categories. If None, uses sort_y parameter.
    sizes : tuple of float, default=(50, 1000)
        Min and max marker sizes in points^2.
    size_norm : tuple of float, optional
        (vmin, vmax) for size normalization. If None, computed from data.
    hue_norm : tuple of float, optional
        (vmin, vmax) for continuous hue normalization. If None, computed from data.
        Providing this parameter enables continuous color mapping.
    alpha : float, default=0.1
        Transparency level for the fill layer (0-1).
    linewidth : float, default=2
        Width of the circle edges.
    edgecolor : str, defaul=None
        Optional edge color. If None, the edge color is the same as the fill color.
    figsize : tuple of float, default=(10, 8)
        Figure size (width, height) in inches.
        If not provided, the figure size will be determined by the data.
        fig, ax = plt.subplots(figsize=(2 * len(nrow), 2 * len(ncol) / 3))
    ax : plt.Axes, optional
        Matplotlib axes object. If None, creates new figure.
    cbar : bool, default=True
        Whether to add a colorbar (for continuous hue only).
    cbar_kws : dict, optional
        Parameters for colorbar appearance (shrink, aspect, pad, etc.).
        Example: {"shrink": 0.5, "aspect": 25, "pad": 0.01}
    size_legend : bool, default=True
        Whether to add a size legend.
    size_legend_title : str, optional
        Title for the size legend. If None, uses size column name.
    hue_legend : bool, default=True
        Whether to add a hue legend (for categorical hue only).
    hue_legend_title : str, optional
        Title for the hue legend. If None, uses hue column name.
    cbar_kws : dict, optional
        Additional keyword arguments for colorbar appearance (shrink, aspect, pad, etc.).
        Example: {"shrink": 0.5, "aspect": 25, "pad": 0.01}
    hue_legend_kws : dict, optional
        Additional keyword arguments for hue legend.
    size_legend_kws : dict, optional
        Additional keyword arguments for size legend.
    title : str, default=""
        Plot title.
    xlabel : str, default=""
        X-axis label. If empty, uses x column name.
    ylabel : str, default=""
        Y-axis label. If empty, uses y column name.
    sort_x : bool, default=True
        Whether to sort x-axis categories alphabetically.
    sort_y : bool, default=True
        Whether to sort y-axis categories alphabetically.
    invert_y : bool, default=True
        Whether to invert y-axis (first category at top).
    grid : bool, default=False
        Whether to show grid lines.
    grid_kws : dict, optional
        Additional keyword arguments for grid.
    xticks_kws : dict, optional
        Additional keyword arguments for x-axis ticks.
    yticks_kws : dict, optional
        Additional keyword arguments for y-axis ticks.
    
    Returns
    -------
    ax : plt.Axes
        The matplotlib axes object.
    cbar : ColorbarBase or None
        The colorbar object if created, otherwise None.
    
    Examples
    --------
    Categorical coloring:
    >>> ax, _ = circle_heatmap(
    ...     data=df,
    ...     x="condition",
    ...     y="pathway",
    ...     size="neg_log10_pval",
    ...     hue="category",
    ...     palette={"A": "blue", "B": "red"}
    ... )
    
    Continuous coloring:
    >>> ax, cbar = circle_heatmap(
    ...     data=df,
    ...     x="sample",
    ...     y="gene",
    ...     size="abs_effect",
    ...     hue="log2fc",
    ...     palette="RdBu_r",
    ...     hue_norm=(-2, 2)
    ... )
    """
    
    # Validate data
    required_cols = [x, y, size, hue]
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in data: {missing_cols}")
    
    # Copy data to avoid modifying original
    data = data.copy()
    
    # Determine if hue is continuous or categorical
    is_continuous_hue = (
        hue_norm is not None or 
        pd.api.types.is_numeric_dtype(data[hue]) # and data[hue].nunique() > 10
    )
    
    # Get unique categories and determine order
    x_cats = _get_ordered_categories(data[x], x_order, sort_x)
    y_cats = _get_ordered_categories(data[y], y_order, sort_y)
    
    # Create position mappings
    x_positions = {cat: i for i, cat in enumerate(x_cats)}
    y_positions = {cat: i for i, cat in enumerate(y_cats)}
    
    # Add position columns
    data["_x_pos"] = data[x].map(x_positions)
    data["_y_pos"] = data[y].map(y_positions)
    
    # Remove rows with unmapped positions
    data = data.dropna(subset=["_x_pos", "_y_pos"])

    # Create axes if not provided
    if ax is None:
        if figsize is None:
            figsize = (
                len(x_cats) * figsize_factors[0], 
                len(y_cats) * figsize_factors[1]
            )
        _, ax = plt.subplots(figsize=figsize)
    
    if len(data) == 0:
        ax.text(0.5, 0.5, "No data to plot", 
                ha="center", va="center", transform=ax.transAxes)
        return ax, None
    
    # Normalize sizes
    data["_size_mapped"], size_ticks, size_norm_obj = _normalize_sizes(
        data[size].values, sizes, size_norm
    )
    
    # Setup color mapping
    if is_continuous_hue:
        palette_mapped, hue_norm_obj = _setup_continuous_palette(
            data[hue].values, palette, hue_norm
        )
    else:
        palette_mapped, hue_cats = _setup_categorical_palette(
            data[hue], palette, hue_order
        )
        hue_norm_obj = None
    
    # Create the scatter plot with double markers
    scatterplot_double_markers(
        data=data,
        x="_x_pos",
        y="_y_pos",
        size="_size_mapped",
        hue=hue,
        palette=palette_mapped,
        hue_norm=hue_norm_obj,
        sizes=(sizes[0], sizes[1]),
        alpha=alpha,
        linewidth=linewidth,
        edgecolor=edgecolor,
        ax=ax,
    )
    
    # Set axis properties
    ax.set_xticks(range(len(x_cats)))
    ax.set_xticklabels(x_cats, **(xticks_kws or {}))
    ax.set_yticks(range(len(y_cats)))
    ax.set_yticklabels(y_cats, **(yticks_kws or {}))
    
    # Set labels
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    # Set axis limits with padding
    ax.set_xlim(-0.5, len(x_cats) - 0.5)
    ax.set_ylim(-0.5, len(y_cats) - 0.5)
    
    # Add grid if requested
    if grid:
        grid_params = {
            **DEFAULT_GRID_KWS,
            **(grid_kws or {}),
        }
        ax.grid(True, **grid_params)
        ax.grid(True, **grid_params)
        ax.set_axisbelow(True)
    
    # Invert y-axis if requested
    if invert_y:
        ax.invert_yaxis()
    
    # Add legends/colorbar
    cbar_obj = None
    legend_end_y = 1
        
    # Add colorbar or categorical hue legend
    if is_continuous_hue and cbar:
        cbar_obj = _add_colorbar(
            ax, hue_norm_obj, palette_mapped, 
            hue_legend_title if hue_legend_title is not None else hue,
            cbar_kws
        )
        # Calculate where colorbar ends (for positioning size legend)
        legend_end_y = _calculate_colorbar_end_y(cbar_kws)
    elif hue_legend:
        hue_legend_kws = hue_legend_kws or {}
        _add_categorical_legend(
            ax, hue_cats, palette_mapped, 
            hue_legend_title if hue_legend_title is not None else hue,
            alpha, linewidth, hue_legend_kws,
        )
        # Estimate categorical legend end position
        n_rows = int(np.ceil(len(hue_cats) / hue_legend_kws.get("ncol", 1)))
        legend_end_y = 1.0 - (n_rows * 0.05 + 0.1)

    # Add size legend if requested
    if size_legend:
        offset_y = max(legend_end_y, 0.2)
        _add_size_legend(
            ax, size_ticks, sizes, size_norm_obj,
            size_legend_title if size_legend_title else size,
            alpha, linewidth, size_legend_kws,
            offset_y=offset_y,
        )

    return ax, cbar_obj


# ============================================================================
# Helper Functions
# ============================================================================

def _get_ordered_categories(
    series: pd.Series,
    order: Optional[List],
    sort: bool
) -> List:
    """Get ordered list of unique categories."""
    if order is not None:
        return order
    
    unique_vals = series.unique()
    if sort:
        return sorted(unique_vals)
    return list(unique_vals)


def _normalize_sizes(
    values: np.ndarray,
    sizes: Tuple[float, float],
    size_norm: Optional[Tuple[float, float]] = None
) -> Tuple[np.ndarray, np.ndarray, Normalize]:
    """
    Normalize size values and compute size legend ticks.
    
    Parameters
    ----------
    values : np.ndarray
        Raw size values.
    sizes : Tuple[float, float]
        (min_size, max_size) in points^2.
    size_norm : Tuple[float, float], optional
        (vmin, vmax) for normalization. If None, computed from data.
    
    Returns
    -------
    sizes_mapped : np.ndarray
        Mapped size values.
    size_ticks : np.ndarray
        Tick values for size legend.
    norm : Normalize
        Normalization object.
    """
    if len(values) == 0:
        return np.array([]), np.array([sizes[0]]), Normalize(vmin=0, vmax=1)
    
    # Determine normalization range
    if size_norm is not None:
        v_min, v_max = size_norm
    else:
        v_min, v_max = float(np.nanmin(values)), float(np.nanmax(values))
    
    norm = Normalize(vmin=v_min, vmax=v_max)
    
    # Normalize and map to size range
    normalized = norm(values)
    sizes_mapped = sizes[0] + normalized * (sizes[1] - sizes[0])
    
    # Generate nice tick values
    locator = MaxNLocator(nbins=4, min_n_ticks=3)
    ticks = locator.tick_values(v_min, v_max)
    ticks = ticks[(ticks >= v_min) & (ticks <= v_max)]
    
    # Round to reasonable precision
    if v_max - v_min > 10:
        ticks = np.unique(np.round(ticks).astype(int))
    else:
        ticks = np.unique(np.round(ticks, 1))
    
    if ticks.size == 0:  # Fallback
        ticks = np.linspace(v_min, v_max, 4)
        ticks = np.unique(np.round(ticks, 1))
    
    return sizes_mapped, ticks, norm


def _setup_continuous_palette(
    values: np.ndarray,
    palette: Optional[Union[str, List]],
    hue_norm: Optional[Tuple[float, float]]
) -> Tuple[Union[str, mpl.colors.Colormap], Normalize]:
    """
    Setup palette and normalization for continuous hue values.
    
    Parameters
    ----------
    values : np.ndarray
        Hue values.
    palette : str, list, or None
        Colormap name or list of colors.
    hue_norm : Tuple[float, float], optional
        (vmin, vmax) for normalization.
    
    Returns
    -------
    palette : str or Colormap
        Color specification for seaborn.
    norm : Normalize
        Normalization object.
    """
    # Determine normalization range
    if hue_norm is not None:
        v_min, v_max = hue_norm
    else:
        v_min, v_max = float(np.nanmin(values)), float(np.nanmax(values))
    
    norm = Normalize(vmin=v_min, vmax=v_max)
    
    # Use provided palette or default
    if palette is None:
        palette = "viridis"
    
    return palette, norm


def _setup_categorical_palette(
    series: pd.Series,
    palette: Optional[Union[str, Dict, List]],
    hue_order: Optional[List]
) -> Tuple[Dict, List]:
    """
    Setup palette for categorical hue values.
    
    Parameters
    ----------
    series : pd.Series
        Hue values.
    palette : str, dict, list, or None
        Color specification.
    hue_order : list, optional
        Order of hue categories.
    
    Returns
    -------
    palette_dict : dict
        Mapping from hue values to colors.
    hue_cats : list
        Ordered list of hue categories.
    """
    # Get ordered categories
    hue_cats = _get_ordered_categories(series, hue_order, sort=True)
    
    # Create palette
    if isinstance(palette, dict):
        palette_dict = palette
    elif isinstance(palette, (list, tuple)):
        palette_dict = {cat: palette[i % len(palette)] 
                       for i, cat in enumerate(hue_cats)}
    elif isinstance(palette, str):
        colors = sns.color_palette(palette, n_colors=len(hue_cats))
        palette_dict = {cat: colors[i] for i, cat in enumerate(hue_cats)}
    else:
        colors = sns.color_palette(n_colors=len(hue_cats))
        palette_dict = {cat: colors[i] for i, cat in enumerate(hue_cats)}
    
    return palette_dict, hue_cats


def _add_colorbar(
    ax: plt.Axes,
    norm: Normalize,
    cmap: Union[str, mpl.colors.Colormap],
    label: str,
    cbar_kws: Optional[Dict]
) -> ColorbarBase:
    """
    Add a colorbar for continuous hue values.
    
    The title is placed at the top of the colorbar (like other legends),
    and the colorbar itself is anchored to the top of the plot area.
    """
    # Default colorbar parameters
    default_params = {
        "ax": ax,
        **DEFAULT_CBAR_KWS
    }
    
    # Merge with user params
    if cbar_kws:
        default_params.update(cbar_kws)
    
    # Get the colormap
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    
    # Create colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    
    cbar = plt.colorbar(sm, **default_params)
    
    # Place label at TOP (like size legend title)
    # Center the label on the colorbar
    cbar.ax.set_title(
        label, 
        pad=10, 
        x=0.0,
        ha="left",
        fontsize=plt.rcParams["legend.fontsize"]
    )
    
    return cbar


def _calculate_colorbar_end_y(cbar_kws: Optional[Dict]) -> float:
    """
    Calculate where the colorbar ends to position size legend right after.
    
    Parameters
    ----------
    cbar_kws : dict, optional
        Colorbar parameters containing shrink value.
    
    Returns
    -------
    float
        Y-coordinate where colorbar ends (for size legend positioning).
    """
    # Get shrink value (default 0.6 if not specified)
    shrink = 0.3
    if cbar_kws and "shrink" in cbar_kws:
        shrink = cbar_kws["shrink"]
    
    # Colorbar is anchored at top (1.0) and extends down by shrink amount
    # Add a small gap (0.05) before size legend
    colorbar_end = 1.0 - shrink - 0.05
    
    return max(colorbar_end, 0.15)  # Don"t go below 0.15


def _add_categorical_legend(
    ax: plt.Axes,
    categories: List,
    palette: Dict,
    title: str,
    alpha: float,
    linewidth: float,
    legend_kws: Optional[Dict],
):
    """Add a legend for categorical hue values."""
    handler = HandlerDoubleCircle(alpha=alpha, linewidth=linewidth)
    
    # Create handles (color, markersize)
    handles = [(palette[cat], 10) for cat in categories]
    
    # Better default positioning to avoid overlap
    legend_params = {
        "bbox_to_anchor": (1.01, 1),
        "loc": "upper left",
        "frameon": False,
        "columnspacing": 1.0,
    }
    if legend_kws:
        legend_params.update(legend_kws)
    
    legend = ax.legend(
        handles=handles,
        labels=categories,
        title=title,
        handler_map={tuple: handler},
        **legend_params
    )
    ax.add_artist(legend)


def _add_size_legend(
    ax: plt.Axes,
    size_ticks: np.ndarray,
    sizes: Tuple[float, float],
    size_norm: Normalize,
    title: str,
    alpha: float,
    linewidth: float,
    legend_kws: Optional[Dict],
    offset_y: float = 0.5
):
    """Add a legend for marker sizes."""
    handler = HandlerDoubleCircle(alpha=alpha, linewidth=linewidth)
    
    # Create handles
    size_handles = []
    size_labels = []
    for tick in size_ticks:
        normalized_size = size_norm(tick)
        actual_size = sizes[0] + normalized_size * (sizes[1] - sizes[0])
        
        # Convert scatter size to markersize for legend
        markersize = np.sqrt(actual_size / np.pi) * 2
        
        size_handles.append(("gray", markersize))
        
        # Format label
        if isinstance(tick, (int, np.integer)):
            size_labels.append(f"{int(tick)}")
        else:
            size_labels.append(f"{tick:.1f}")
    
    # Better default positioning to avoid overlap
    legend_kws = legend_kws or {}

    # Reverse the order of the legend if requested
    reverse = (legend_kws or {}).pop("reverse", True)
    if reverse:
        size_handles.reverse()
        size_labels.reverse()

    legend_params = {
        "bbox_to_anchor": (1.01, offset_y),
        "loc": "upper left",
        "frameon": False,
        "labelspacing": 1.5 if legend_kws.get("ncol", 1) == 1 else 1.0,
        "columnspacing": 1.0,
        **legend_kws
    }
    
    ax.legend(
        handles=size_handles,
        labels=size_labels,
        title=title,
        handler_map={tuple: handler},
        **legend_params
    )