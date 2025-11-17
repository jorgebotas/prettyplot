"""
Color palettes for publiplots.

This module provides carefully curated color palettes optimized for
publication-ready visualizations, with seamless integration with seaborn.
"""

from typing import Dict, List, Optional, Union

from publiplots.themes.rcparams import resolve_param
from publiplots.utils import is_categorical

# =============================================================================
# Color Palettes
# =============================================================================

PALETTES = {
    "pastel": [
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
}
"""Dictionary of custom publiplots palettes."""


# =============================================================================
# Functions
# =============================================================================

def color_palette(palette=None, n_colors=None, desat=None, as_cmap=False):
    """
    Return a color palette as a list of hex colors or colormap.

    Integrates with seaborn - custom publiplots palettes override seaborn defaults.

    Parameters
    ----------
    palette : str, list, or None
        Palette name (checks publiplots first, then seaborn) or list of colors.
        If None, uses the default palette from rcParams.
    n_colors : int, optional
        Number of colors in the palette.
    desat : float, optional
        Proportion to desaturate each color.
    as_cmap : bool, default=False
        If True, return a matplotlib colormap instead of a list.

    Returns
    -------
    list or matplotlib.colors.ListedColormap
        List of hex color codes or colormap if as_cmap=True.

    Examples
    --------
    Get custom pastel palette:
    >>> colors = color_palette("pastel")
    >>> len(colors)
    12

    Get seaborn palette:
    >>> colors = color_palette("viridis", n_colors=5)

    Get as colormap:
    >>> cmap = color_palette("pastel", as_cmap=True)
    """
    import seaborn as sns

    # Handle None: use default palette from rcParams
    if palette is None:
        palette = resolve_param("palette", "pastel")

    # Check publiplots PALETTES first
    if isinstance(palette, str) and palette in PALETTES:
        colors = PALETTES[palette]
        if as_cmap:
            from matplotlib.colors import ListedColormap
            return ListedColormap(colors)
        return sns.color_palette(colors, n_colors=n_colors, desat=desat)

    # Delegate everything else to seaborn
    return sns.color_palette(palette, n_colors=n_colors, desat=desat, as_cmap=as_cmap)


def resolve_palette_mapping(
    values: Optional[List[str]] = None,
    palette: Optional[Union[str, Dict, List]] = None,
) -> Dict[str, str]:
    """
    Resolve a palette mapping to actual colors (internal helper).

    Maps categorical values to colors, handling various palette specifications.

    Parameters
    ----------
    values : List[str], optional
        List of categorical values to map to colors.
    palette : str, dict, or list, optional
        Palette specification:
        - None: Uses default palette
        - str: Palette name (checks publiplots first, then seaborn)
        - list: List of color hex codes
        - dict: Pre-mapped categories to colors (returned as-is)

    Returns
    -------
    Dict[str, str]
        Dictionary mapping each value to a color.
    """
    if values is None:
        return {}
    if isinstance(palette, dict):
        return palette
    if not is_categorical(values):
        return palette  # continuous mapping

    # Use color_palette internally
    palette = color_palette(palette, n_colors=len(values))
    return {value: palette[i % len(palette)] for i, value in enumerate(values)}
