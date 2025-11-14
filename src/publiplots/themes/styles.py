"""
Matplotlib style presets for publiplots.

This module provides functions to apply consistent styling to matplotlib
plots, optimized for publication-ready visualizations.
"""

from typing import  Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams


# =============================================================================
# Style Dictionaries
# =============================================================================


ILLUSTRATOR_STYLE: Dict[str, Any] = {
    # Font settings
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.labelsize": 8,
    "axes.titlesize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "legend.title_fontsize": 9,
    "figure.titlesize": 10,

    # PDF settings (for vector graphics)
    "pdf.fonttype": 42,
    "ps.fonttype": 42,

    # Figure settings
    "figure.figsize": (3.5, 2.5),
    "figure.dpi": 100,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,

    # Axes settings
    "axes.linewidth": 0.75,
    "axes.edgecolor": "0.3",
    "axes.labelcolor": "0.3",
    "axes.grid": False,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "axes.axisbelow": True,

    # Grid settings
    "grid.color": "0.8",
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,

    # Tick settings
    "xtick.major.width": 1,
    "ytick.major.width": 1,
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "xtick.color": "0.3",
    "ytick.color": "0.3",
    "xtick.direction": "out",
    "ytick.direction": "out",

    # Legend settings
    "legend.frameon": False,
    "legend.numpoints": 1,
    "legend.scatterpoints": 1,

    # Line settings
    "lines.linewidth": 1,
    "lines.markersize": 8,

    # Patch settings (for bars, etc.)
    "patch.linewidth": 1,
    "patch.edgecolor": "0.3",
}

PUBLICATION_STYLE: Dict[str, Any] = {
    # Font settings
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "legend.title_fontsize": 12,
    "figure.titlesize": 14,

    # PDF settings (for vector graphics)
    "pdf.fonttype": 42,
    "ps.fonttype": 42,

    # Figure settings
    "figure.figsize": (6, 4),
    "figure.dpi": 100,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,

    # Axes settings
    "axes.linewidth": 1.5,
    "axes.edgecolor": "0.2",
    "axes.labelcolor": "0.2",
    "axes.grid": False,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "axes.axisbelow": True,

    # Grid settings
    "grid.color": "0.8",
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,

    # Tick settings
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5,
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "xtick.color": "0.2",
    "ytick.color": "0.2",
    "xtick.direction": "out",
    "ytick.direction": "out",

    # Legend settings
    "legend.frameon": False,
    "legend.numpoints": 1,
    "legend.scatterpoints": 1,

    # Line settings
    "lines.linewidth": 2.0,
    "lines.markersize": 8,

    # Patch settings (for bars, etc.)
    "patch.linewidth": 2.0,
    "patch.edgecolor": "0.2",
}
"""
Publication-ready style optimized for scientific papers and presentations.

Features:
- Clean sans-serif fonts (Arial preferred)
- High DPI for crisp output
- Minimal spines (top and right removed)
- Appropriate sizing for standard figure widths
"""

MINIMAL_STYLE: Dict[str, Any] = {
    **PUBLICATION_STYLE,
    # More minimal - even fewer visual elements
    "axes.linewidth": 1.0,
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "lines.linewidth": 1.5,
}
"""
Minimal style with reduced visual clutter.

Lighter lines and simpler appearance, ideal for presentations or
when multiple figures need to be displayed together.
"""

POSTER_STYLE: Dict[str, Any] = {
    **PUBLICATION_STYLE,
    # Larger sizes for poster presentations
    "font.size": 16,
    "axes.labelsize": 18,
    "axes.titlesize": 20,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "legend.title_fontsize": 16,
    "figure.titlesize": 22,
    "figure.figsize": (8, 6),
    "lines.linewidth": 3.0,
    "lines.markersize": 10,
    "axes.linewidth": 2.0,
    "xtick.major.width": 2.0,
    "ytick.major.width": 2.0,
    "patch.linewidth": 3.0,
}
"""
Poster presentation style with larger fonts and thicker lines.

Optimized for viewing from a distance, such as conference posters
or large-screen presentations.
"""


# =============================================================================
# Functions
# =============================================================================

def set_publication_style(
    font: str = "Arial",
    font_scale: float = 1.6,
    context: str = "paper",
    palette: str = "pastel_categorical"
) -> None:
    """
    Apply publication-ready style to all matplotlib plots.

    This is the main styling function that should be called at the beginning
    of a script to ensure consistent, publication-ready plots.

    Parameters
    ----------
    font : str, default='Arial'
        Font family to use. Common options: 'Arial', 'Helvetica', 'Times'.
    font_scale : float, default=1.0
        Scaling factor for all font sizes. Use >1 for larger fonts.
    context : str, default='paper'
        Seaborn context: 'paper', 'notebook', 'talk', or 'poster'.
    palette : str, default='pastel_categorical'
        Default color palette name from publiplots.themes.colors.

    Examples
    --------
    Apply default publication style:
    >>> import publiplots as pp
    >>> pp.set_publication_style()

    Use larger fonts for a presentation:
    >>> pp.set_publication_style(font_scale=1.3, context='talk')

    Use Times font for a specific journal:
    >>> pp.set_publication_style(font='Times New Roman')
    """
    # Apply seaborn style first
    sns.set_theme(context=context, style="white", font=font, font_scale=font_scale)

    # Apply publiplots style
    for key, value in PUBLICATION_STYLE.items():
        rcParams[key] = value

    # Override font if specified
    if font != "Arial":
        rcParams["font.sans-serif"] = [font, "Arial", "Helvetica", "DejaVu Sans"]

    # Apply font scaling
    if font_scale != 1.0:
        for key in rcParams.keys():
            if 'size' in key and isinstance(rcParams[key], (int, float)):
                rcParams[key] = rcParams[key] * font_scale

    # Set default color palette
    from publiplots.themes.colors import get_palette
    try:
        colors = get_palette(palette)
        if isinstance(colors, list):
            sns.set_palette(colors)
    except ValueError:
        pass  # If palette doesn't exist, keep seaborn default


def set_illustrator_style(
    font: str = "Arial",
    font_scale: float = 1.0,
    context: str = "paper",
    palette: str = "pastel_categorical"
) -> None:
    """
    Apply illustrator-ready style to all matplotlib plots.

    This is the main styling function that should be called at the beginning
    of a script to ensure consistent, illustrator-ready plots.

    Parameters
    ----------
    font : str, default='Arial'
        Font family to use. Common options: 'Arial', 'Helvetica', 'Times'.
    font_scale : float, default=1.0
        Scaling factor for all font sizes. Use >1 for larger fonts.
    context : str, default='paper'
        Seaborn context: 'paper', 'notebook', 'talk', or 'poster'.
    palette : str, default='pastel_categorical'
        Default color palette name from publiplots.themes.colors.

    Examples
    --------
    Apply default illustrator style:
    >>> import publiplots as pp
    >>> pp.set_illustrator_style()

    Use larger fonts for a presentation:
    >>> pp.set_illustrator_style(font_scale=1.3, context='talk')

    Use Times font for a specific journal:
    >>> pp.set_illustrator_style(font='Times New Roman')
    """
    # Apply seaborn style first
    sns.set_theme(context=context, style="white", font=font, font_scale=font_scale)

    # Apply publiplots style
    for key, value in ILLUSTRATOR_STYLE.items():
        rcParams[key] = value

    # Override font if specified
    if font != "Arial":
        rcParams["font.sans-serif"] = [font, "Arial", "Helvetica", "DejaVu Sans"]

    # Apply font scaling
    if font_scale != 1.0:
        for key in rcParams.keys():
            if 'size' in key and isinstance(rcParams[key], (int, float)):
                rcParams[key] = rcParams[key] * font_scale

    # Set default color palette
    from publiplots.themes.colors import get_palette
    try:
        colors = get_palette(palette)
        if isinstance(colors, list):
            sns.set_palette(colors)
    except ValueError:
        pass  # If palette doesn't exist, keep seaborn default

def set_minimal_style(
    font: str = "Arial",
    font_scale: float = 1.0
) -> None:
    """
    Apply minimal style with reduced visual elements.

    Parameters
    ----------
    font : str, default='Arial'
        Font family to use.
    font_scale : float, default=1.0
        Scaling factor for all font sizes.

    Examples
    --------
    >>> import publiplots as pp
    >>> pp.set_minimal_style()
    """
    sns.set_theme(context="paper", style="white", font=font, font_scale=font_scale)

    for key, value in MINIMAL_STYLE.items():
        rcParams[key] = value

    if font != "Arial":
        rcParams["font.sans-serif"] = [font, "Arial", "Helvetica", "DejaVu Sans"]

    if font_scale != 1.0:
        for key in rcParams.keys():
            if 'size' in key and isinstance(rcParams[key], (int, float)):
                rcParams[key] = rcParams[key] * font_scale


def set_poster_style(
    font: str = "Arial",
    font_scale: float = 2.0,
    palette: str = "pastel_categorical"
) -> None:
    """
    Apply poster presentation style with larger elements.

    Parameters
    ----------
    font : str, default='Arial'
        Font family to use.
    font_scale : float, default=1.0
        Additional scaling factor on top of poster defaults.
    palette : str, default='pastel_categorical'
        Default color palette name.

    Examples
    --------
    >>> import publiplots as pp
    >>> pp.set_poster_style()
    """
    sns.set_theme(context="poster", style="white", font=font, font_scale=font_scale)

    for key, value in POSTER_STYLE.items():
        rcParams[key] = value

    if font != "Arial":
        rcParams["font.sans-serif"] = [font, "Arial", "Helvetica", "DejaVu Sans"]

    if font_scale != 1.0:
        for key in rcParams.keys():
            if 'size' in key and isinstance(rcParams[key], (int, float)):
                rcParams[key] = rcParams[key] * font_scale

    from publiplots.themes.colors import get_palette
    try:
        colors = get_palette(palette)
        if isinstance(colors, list):
            sns.set_palette(colors)
    except ValueError:
        pass


def reset_style() -> None:
    """
    Reset matplotlib rcParams to defaults.

    Useful when you want to revert to matplotlib's default styling.

    Examples
    --------
    >>> import publiplots as pp
    >>> pp.set_publication_style()
    >>> # ... create plots ...
    >>> pp.reset_style()  # Reset to defaults
    """
    plt.rcdefaults()
    sns.reset_defaults()


def get_current_style() -> Dict[str, Any]:
    """
    Get current matplotlib rcParams as a dictionary.

    Useful for debugging or saving current style settings.

    Returns
    -------
    Dict[str, Any]
        Dictionary of current rcParams.

    Examples
    --------
    >>> import publiplots as pp
    >>> pp.set_publication_style()
    >>> current = pp.get_current_style()
    >>> print(current['font.size'])
    11
    """
    return dict(rcParams)


def apply_custom_style(style_dict: Dict[str, Any]) -> None:
    """
    Apply a custom style dictionary to matplotlib.

    Parameters
    ----------
    style_dict : Dict[str, Any]
        Dictionary of matplotlib rcParams to apply.

    Examples
    --------
    >>> import publiplots as pp
    >>> custom = {'font.size': 14, 'lines.linewidth': 3}
    >>> pp.apply_custom_style(custom)
    """
    for key, value in style_dict.items():
        rcParams[key] = value
