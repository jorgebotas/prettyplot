"""
Default rcParams settings for publiplots.

This module defines the default matplotlib rcParams that will be initialized
when publiplots is imported. All publiplots functions read from these rcParams,
ensuring consistency with matplotlib/seaborn styling patterns.
"""

from typing import Dict, Any
import matplotlib.pyplot as plt


# =============================================================================
# PubliPlots Default rcParams
# =============================================================================

# Standard matplotlib rcParams that publiplots sets
PUBLIPLOTS_RCPARAMS: Dict[str, Any] = {
    # Figure settings - small defaults suitable for publications
    "figure.figsize": (3, 2),
    "figure.dpi": 100,  # Display DPI
    "savefig.dpi": 300,  # Output DPI
    "savefig.format": "pdf",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,

    # Font settings - publication-ready defaults
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],

    # Line settings
    "lines.linewidth": 1.0,
    "lines.markersize": 8,

    # PDF settings for vector graphics (editable text in Adobe Illustrator)
    "pdf.fonttype": 42,
    "ps.fonttype": 42,

    # Patch settings (for bars, etc.)
    "patch.linewidth": 1.0,
}

# Custom publiplots settings (not part of matplotlib rcParams)
# These are stored as module-level variables since matplotlib doesn't support custom namespaces
_PUBLIPLOTS_CUSTOM_DEFAULTS: Dict[str, Any] = {
    "color": "#5d83c3",  # Default slate blue color
    "alpha": 0.1,  # Default transparency for error bars/bands
    "capsize": 0.0,  # Default error bar cap size
    "palette": "pastel_categorical",  # Default color palette name
    "hatch_mode": 1,  # Default hatch pattern density mode
}
"""
Default rcParams for publiplots.

These settings are automatically applied when publiplots is imported,
providing sensible publication-ready defaults that can be overridden
by style functions or manual rcParams updates.

Standard matplotlib rcParams:
- figure.figsize: (3, 2) - Compact figures suitable for publications
- figure.dpi: 100 - Display resolution
- savefig.dpi: 300 - High-quality output for publications
- savefig.format: 'pdf' - Vector format for scalability
- lines.linewidth: 1.0 - Moderate line thickness
- pdf.fonttype: 42 - TrueType fonts (editable in Illustrator)

Custom publiplots rcParams (use 'publiplots.*' namespace):
- publiplots.color: Default color for single-color plots
- publiplots.alpha: Default transparency for error regions
- publiplots.capsize: Default error bar cap size
- publiplots.palette: Default categorical color palette name
- publiplots.hatch_mode: Hatch pattern density mode (1=normal, 2=dense)
"""


# =============================================================================
# Initialization Functions
# =============================================================================

def init_rcparams() -> None:
    """
    Initialize publiplots default rcParams.

    This function is automatically called when publiplots is imported.
    It sets sensible defaults for standard matplotlib rcParams without
    overwriting user customizations that may have been applied before import.

    Examples
    --------
    Manually reinitialize defaults:
    >>> import publiplots as pp
    >>> pp.themes.defaults.init_rcparams()

    Reset to publiplots defaults after using other styles:
    >>> import matplotlib.pyplot as plt
    >>> plt.style.use('default')
    >>> pp.themes.defaults.init_rcparams()
    """
    for key, value in PUBLIPLOTS_RCPARAMS.items():
        # Only set if key doesn't exist or is at matplotlib default
        # This preserves user customizations made before import
        if key not in plt.rcParams or plt.rcParams[key] == plt.rcParamsDefault.get(key):
            plt.rcParams[key] = value


def get_default(key: str, fallback: Any = None) -> Any:
    """
    Get a publiplots default value.

    For standard matplotlib rcParams (e.g., 'figure.figsize'), reads from plt.rcParams.
    For custom publiplots settings (e.g., 'color', 'alpha'), reads from internal defaults.

    Parameters
    ----------
    key : str
        The parameter key. Can be a full rcParam key (e.g., 'figure.figsize')
        or a custom publiplots key (e.g., 'color', 'alpha', 'palette').
    fallback : Any, optional
        Fallback value if the key doesn't exist.

    Returns
    -------
    Any
        The parameter value, or fallback if not found.

    Examples
    --------
    Get figure size:
    >>> from publiplots.themes.defaults import get_default
    >>> figsize = get_default('figure.figsize')
    >>> print(figsize)
    (3, 2)

    Get custom parameter:
    >>> alpha = get_default('alpha')
    >>> print(alpha)
    0.1
    """
    # Check if it's a custom publiplots parameter
    if key in _PUBLIPLOTS_CUSTOM_DEFAULTS:
        return _PUBLIPLOTS_CUSTOM_DEFAULTS.get(key, fallback)

    # Otherwise, check matplotlib rcParams
    if fallback is None:
        fallback = PUBLIPLOTS_RCPARAMS.get(key)
    return plt.rcParams.get(key, fallback)


def reset_to_publiplots_defaults() -> None:
    """
    Reset all publiplots rcParams to their default values.

    Unlike init_rcparams(), this function forcefully overwrites
    all publiplots-related rcParams, restoring the original defaults.

    Examples
    --------
    Reset after experimenting with different settings:
    >>> import publiplots as pp
    >>> import matplotlib.pyplot as plt
    >>> plt.rcParams['figure.figsize'] = (10, 10)  # Custom setting
    >>> pp.themes.defaults.reset_to_publiplots_defaults()
    >>> print(plt.rcParams['figure.figsize'])
    (3, 2)
    """
    for key, value in PUBLIPLOTS_RCPARAMS.items():
        plt.rcParams[key] = value


def get_publiplots_rcparam(key: str, default: Any = None) -> Any:
    """
    Get a publiplots rcParam value with fallback to default.

    This is a convenience function for accessing publiplots-specific
    rcParams with type safety and default fallback.

    Parameters
    ----------
    key : str
        The rcParam key to retrieve. For publiplots-specific params,
        use 'publiplots.param_name'. For standard matplotlib params,
        use the standard key (e.g., 'figure.figsize').
    default : Any, optional
        Fallback value if the key doesn't exist in rcParams.
        If not provided, uses the default from PUBLIPLOTS_RCPARAMS.

    Returns
    -------
    Any
        The rcParam value, or default if not found.

    Examples
    --------
    Get figure size:
    >>> from publiplots.themes.defaults import get_publiplots_rcparam
    >>> figsize = get_publiplots_rcparam('figure.figsize')
    >>> print(figsize)
    (3, 2)

    Get custom parameter with fallback:
    >>> alpha = get_publiplots_rcparam('publiplots.alpha', 0.2)
    >>> print(alpha)
    0.1
    """
    if default is None:
        default = PUBLIPLOTS_RCPARAMS.get(key)
    return plt.rcParams.get(key, default)
