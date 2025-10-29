"""
Color palettes for prettyplot.

This module provides carefully curated color palettes optimized for
publication-ready visualizations, with a focus on pastel colors that
are visually appealing and print well.
"""

from typing import Dict, List, Optional, Union
import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# Default Color
# =============================================================================

DEFAULT_COLOR: str = "#5d83c3"
"""
Default color for single-color plots.

This slate blue color is used as the default when no palette or color
is specified. It provides a professional, publication-ready appearance
while being distinct and visually appealing.
"""


# =============================================================================
# Categorical Palettes
# =============================================================================

PASTEL_CATEGORICAL: List[str] = [
    "#75b375",  # Soft green
    "#8e8ec1",  # Soft purple
    "#eeaa58",  # Soft orange
    "#e67e7e",  # Soft red
    "#7ec5d9",  # Soft blue
    "#f0b0c4",  # Soft pink
    "#b8b88a",  # Soft olive
    "#c9a3cf",  # Soft lavender
    "#f4c896",  # Soft peach
    "#8fc9a8",  # Soft teal
    "#dba3a3",  # Soft rose
    "#9eb3d4",  # Soft periwinkle
]
"""
Pastel categorical palette with 12 distinct colors.

Use case: Categorical data with multiple distinct groups.
Works well for bar plots, scatter plots with categorical hue, and legends.
Colors are designed to be distinguishable while maintaining a soft, cohesive look.

Example:
    >>> import prettyplot as pp
    >>> colors = pp.get_palette('pastel_categorical', n_colors=5)
    >>> pp.scatterplot(data=df, x='x', y='y', hue='category', palette=colors)
"""

PASTEL_CATEGORICAL_MINIMAL: List[str] = [
    "#75b375",  # Soft green
    "#8e8ec1",  # Soft purple
    "#eeaa58",  # Soft orange
    "#7ec5d9",  # Soft blue
]
"""
Minimal pastel categorical palette with 4 colors.

Use case: Small number of categories (2-4).
Optimized for clarity when fewer distinct groups need to be shown.

Example:
    >>> colors = pp.get_palette('pastel_categorical_minimal', n_colors=3)
"""

# =============================================================================
# Sequential Palettes
# =============================================================================

PASTEL_SEQUENTIAL_GREEN: List[str] = [
    "#e8f5e8",
    "#c8e6c8",
    "#a8d7a8",
    "#88c888",
    "#68b968",
    "#4aa44a",
]
"""
Sequential green palette (light to dark).

Use case: Continuous data ranging from low to high values.
Ideal for heatmaps, choropleth maps, and representing intensity.
"""

PASTEL_SEQUENTIAL_BLUE: List[str] = [
    "#e8f4f8",
    "#c8e4f0",
    "#a8d4e8",
    "#88c4e0",
    "#68b4d8",
    "#4aa4d0",
]
"""
Sequential blue palette (light to dark).

Use case: Continuous data, alternative to green for variety or when
representing different data types in the same figure.
"""

PASTEL_SEQUENTIAL_PURPLE: List[str] = [
    "#f0e8f5",
    "#e0c8e6",
    "#d0a8d7",
    "#c088c8",
    "#b068b9",
    "#a048a4",
]
"""
Sequential purple palette (light to dark).

Use case: Continuous data, provides good contrast with green/blue palettes
when multiple sequential scales are needed in complex visualizations.
"""

# =============================================================================
# Diverging Palettes
# =============================================================================

PASTEL_DIVERGING_RED_BLUE: List[str] = [
    "#e67e7e",  # Soft red
    "#f4a4a4",
    "#ffd4d4",
    "#f5f5f5",  # Neutral gray
    "#d4e4ff",
    "#a4c4f4",
    "#7ec5d9",  # Soft blue
]
"""
Diverging red-blue palette.

Use case: Data with a meaningful center point (e.g., zero, mean, or neutral value).
Perfect for log fold changes, correlations, or any data where deviation from
center in either direction has different meanings.

Example:
    >>> colors = pp.get_palette('pastel_diverging_red_blue', n_colors=7)
    >>> pp.heatmap(data=df, palette=colors, center=0)
"""

PASTEL_DIVERGING_GREEN_PURPLE: List[str] = [
    "#75b375",  # Soft green
    "#98c898",
    "#c8e6c8",
    "#f5f5f5",  # Neutral gray
    "#e8d8f0",
    "#c8a8d7",
    "#8e8ec1",  # Soft purple
]
"""
Diverging green-purple palette.

Use case: Alternative to red-blue for diverging data, especially useful
when red-green colorblindness is a concern or when red-blue is already
used for another data dimension.
"""

# =============================================================================
# Special Purpose Palettes
# =============================================================================

PASTEL_SIGNIFICANCE: Dict[str, str] = {
    "significant": "#75b375",      # Green for significant
    "not_significant": "#999999",  # Gray for not significant
    "highly_significant": "#4aa44a",  # Darker green for highly significant
}
"""
Significance palette for p-value visualization.

Use case: Highlighting statistically significant results in enrichment
analyses, differential expression, or other hypothesis testing visualizations.

Example:
    >>> colors = pp.PASTEL_SIGNIFICANCE
    >>> pp.barplot_enrichment(categories=terms, values=scores,
    ...                       pvalues=pvals, significance_colors=colors)
"""

PASTEL_POSITIVE_NEGATIVE: Dict[str, str] = {
    "positive": "#75b375",  # Green
    "negative": "#e67e7e",  # Red
    "neutral": "#eeaa58",   # Orange
}
"""
Positive/negative/neutral palette.

Use case: Data with clear positive and negative values (e.g., correlation,
fold change, effect size) where neutral represents ambiguous or intermediate state.
"""

# =============================================================================
# Palette Dictionary
# =============================================================================

PALETTES: Dict[str, Union[List[str], Dict[str, str]]] = {
    "pastel_categorical": PASTEL_CATEGORICAL,
    "pastel_categorical_minimal": PASTEL_CATEGORICAL_MINIMAL,
    "pastel_sequential_green": PASTEL_SEQUENTIAL_GREEN,
    "pastel_sequential_blue": PASTEL_SEQUENTIAL_BLUE,
    "pastel_sequential_purple": PASTEL_SEQUENTIAL_PURPLE,
    "pastel_diverging_red_blue": PASTEL_DIVERGING_RED_BLUE,
    "pastel_diverging_green_purple": PASTEL_DIVERGING_GREEN_PURPLE,
    "pastel_significance": PASTEL_SIGNIFICANCE,
    "pastel_positive_negative": PASTEL_POSITIVE_NEGATIVE,
}
"""Dictionary of all available palettes."""


# =============================================================================
# Functions
# =============================================================================

def get_palette(
    name: str,
    n_colors: Optional[int] = None,
    reverse: bool = False
) -> Union[List[str], Dict[str, str]]:
    """
    Get a color palette by name.

    Parameters
    ----------
    name : str
        Name of the palette. Available palettes:
        - 'pastel_categorical': 12 distinct pastel colors
        - 'pastel_categorical_minimal': 4 colors for minimal categories
        - 'pastel_sequential_green': Sequential green palette
        - 'pastel_sequential_blue': Sequential blue palette
        - 'pastel_sequential_purple': Sequential purple palette
        - 'pastel_diverging_red_blue': Red-blue diverging palette
        - 'pastel_diverging_green_purple': Green-purple diverging palette
        - 'pastel_significance': Significance levels (dict)
        - 'pastel_positive_negative': Positive/negative/neutral (dict)
    n_colors : int, optional
        Number of colors to return. If None, returns all colors in the palette.
        For sequential/diverging palettes, interpolates to get exact number.
        Not applicable for dictionary palettes.
    reverse : bool, default=False
        Whether to reverse the palette order.

    Returns
    -------
    Union[List[str], Dict[str, str]]
        List of color hex codes or dictionary mapping names to colors.

    Raises
    ------
    ValueError
        If palette name is not found or n_colors is invalid.

    Examples
    --------
    Get a categorical palette:
    >>> colors = get_palette('pastel_categorical', n_colors=5)
    >>> len(colors)
    5

    Get a sequential palette with interpolation:
    >>> colors = get_palette('pastel_sequential_green', n_colors=10)

    Get a significance palette (returns dict):
    >>> colors = get_palette('pastel_significance')
    >>> colors['significant']
    '#75b375'
    """
    if name not in PALETTES:
        available = ', '.join(PALETTES.keys())
        raise ValueError(f"Unknown palette '{name}'. Available palettes: {available}")

    palette = PALETTES[name]

    # Handle dictionary palettes
    if isinstance(palette, dict):
        if n_colors is not None:
            raise ValueError(
                f"Palette '{name}' is a dictionary palette. "
                "n_colors parameter is not applicable."
            )
        return palette

    # Handle list palettes
    if n_colors is None:
        result = list(palette)
    elif n_colors <= len(palette):
        # Return subset of palette
        result = list(palette[:n_colors])
    else:
        # Interpolate to get more colors
        result = _interpolate_colors(palette, n_colors)

    if reverse:
        result = result[::-1]

    return result


def _interpolate_colors(colors: List[str], n: int) -> List[str]:
    """
    Interpolate between colors to create a palette with n colors.

    Parameters
    ----------
    colors : List[str]
        List of hex color codes to interpolate between.
    n : int
        Number of colors to generate.

    Returns
    -------
    List[str]
        List of n interpolated hex color codes.
    """
    from matplotlib.colors import LinearSegmentedColormap, to_hex

    # Create a colormap from the colors
    cmap = LinearSegmentedColormap.from_list("custom", colors, N=n)

    # Sample n colors from the colormap
    indices = np.linspace(0, 1, n)
    interpolated = [to_hex(cmap(idx)) for idx in indices]

    return interpolated


def resolve_palette(
    palette: Optional[Union[str, List[str], Dict[str, str]]] = None,
    n_colors: Optional[int] = None
) -> Union[List[str], Dict[str, str]]:
    """
    Resolve a palette to actual colors, supporting both prettyplot and seaborn palettes.

    This helper function translates palette specifications to actual color values.
    It checks if a string palette name is a prettyplot palette first, then falls
    back to seaborn palettes if not found.

    Parameters
    ----------
    palette : str, list, dict, or None
        Palette specification:
        - None: Returns default palette (or default color for n_colors=1)
        - str: Palette name (checks prettyplot first, then seaborn)
        - list: List of color hex codes (returned as-is)
        - dict: Mapping from categories to colors (returned as-is)
    n_colors : int, optional
        Number of colors to return. Only applicable for string palette names.

    Returns
    -------
    Union[List[str], Dict[str, str]]
        Resolved palette as list of colors or dictionary.

    Examples
    --------
    Get default color for single-color plots:
    >>> colors = resolve_palette(n_colors=1)
    >>> colors
    ['#5d83c3']

    Get default palette for multi-color plots:
    >>> colors = resolve_palette(n_colors=3)
    >>> len(colors)
    3

    Resolve prettyplot palette:
    >>> colors = resolve_palette('pastel_categorical', n_colors=5)

    Resolve seaborn palette:
    >>> colors = resolve_palette('viridis', n_colors=5)

    Pass through color list:
    >>> colors = resolve_palette(['#ff0000', '#00ff00', '#0000ff'])
    ['#ff0000', '#00ff00', '#0000ff']
    """
    import seaborn as sns
    from prettyplot.config import DEFAULT_PALETTE

    # Handle None: use default palette for multiple colors, default color for single
    if palette is None:
        if n_colors is not None and n_colors > 1:
            # Use default palette for multiple colors
            return get_palette(DEFAULT_PALETTE, n_colors=n_colors)
        else:
            # Use default color for single color
            return [DEFAULT_COLOR]

    # Handle list/dict: return as-is
    if isinstance(palette, (list, dict)):
        return palette

    # Handle string: check prettyplot first, then seaborn
    if isinstance(palette, str):
        # Try prettyplot palette first
        if palette in PALETTES:
            return get_palette(palette, n_colors=n_colors)

        # Fall back to seaborn palette
        try:
            if n_colors is not None:
                return sns.color_palette(palette, n_colors=n_colors).as_hex()
            else:
                return sns.color_palette(palette).as_hex()
        except Exception as e:
            raise ValueError(
                f"Unknown palette '{palette}'. Not found in prettyplot palettes "
                f"({', '.join(PALETTES.keys())}) or seaborn palettes. Error: {e}"
            )

    # Should not reach here
    raise ValueError(f"Invalid palette type: {type(palette)}")


def list_palettes() -> List[str]:
    """
    List all available palette names.

    Returns
    -------
    List[str]
        List of available palette names.

    Examples
    --------
    >>> palettes = list_palettes()
    >>> print(palettes)
    ['pastel_categorical', 'pastel_sequential_green', ...]
    """
    return list(PALETTES.keys())


def show_palette(name: str, n_colors: Optional[int] = None) -> None:
    """
    Display a color palette visually.

    Creates a simple visualization showing the colors in the palette.
    Useful for exploring and comparing palettes.

    Parameters
    ----------
    name : str
        Name of the palette to display.
    n_colors : int, optional
        Number of colors to display. If None, shows all colors.

    Examples
    --------
    >>> show_palette('pastel_categorical')
    >>> show_palette('pastel_sequential_green', n_colors=10)
    """
    palette = get_palette(name, n_colors)

    if isinstance(palette, dict):
        # Display dictionary palette
        colors_list = list(palette.values())
        labels = list(palette.keys())
        n = len(colors_list)
    else:
        colors_list = palette
        labels = [f"{i+1}" for i in range(len(colors_list))]
        n = len(colors_list)

    # Create visualization
    fig, ax = plt.subplots(figsize=(n * 0.8, 2))

    for i, (color, label) in enumerate(zip(colors_list, labels)):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))
        ax.text(i + 0.5, 0.5, label, ha='center', va='center',
                fontsize=10, rotation=90 if len(label) > 3 else 0)

    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"Palette: {name}", fontsize=14, pad=10)

    plt.tight_layout()
    plt.show()
