"""
Default rcParams settings for publiplots.

This module defines the default matplotlib rcParams that will be initialized
when publiplots is imported. All publiplots functions read from these rcParams,
ensuring consistency with matplotlib/seaborn styling patterns.

Base defaults are defined in base_defaults.py and composed into styles.

Main exports:
- rcParams: Unified parameter interface (pp.rcParams['color'])
- resolve_param(): Helper to resolve parameter values (value or default)
- get_default(): Direct access to default values
"""

from typing import Dict, Any, Optional
import matplotlib.pyplot as plt

from .base_defaults import MATPLOTLIB_DEFAULTS, CUSTOM_DEFAULTS


# =============================================================================
# PubliPlots Default rcParams
# =============================================================================

# Standard matplotlib rcParams (imported from base_defaults)
PUBLIPLOTS_RCPARAMS: Dict[str, Any] = MATPLOTLIB_DEFAULTS
"""
Default matplotlib rcParams for publiplots.

These are the base defaults shared across all styles. Individual styles
(notebook, publication) may override specific parameters.

See base_defaults.py for the complete list of default values.
"""

# Custom publiplots settings (not part of matplotlib rcParams)
# These are stored as module-level variables since matplotlib doesn't support custom namespaces
# Start with a copy so styles can modify without affecting the base
_PUBLIPLOTS_CUSTOM_DEFAULTS: Dict[str, Any] = CUSTOM_DEFAULTS.copy()
"""
Custom publiplots parameters.

These parameters are not part of matplotlib's rcParams but are used by
publiplots functions. They can be accessed and modified via pp.rcParams.

Current custom parameters:
- color: Default color for single-color plots
- alpha: Default transparency for bars/error regions
- capsize: Default error bar cap size
- palette: Default categorical color palette name
- hatch_mode: Hatch pattern density mode (1-4)
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


# =============================================================================
# PubliPlots rcParams Wrapper
# =============================================================================

class PubliplotsRcParams:
    """
    Unified interface for publiplots parameters.

    This class provides a dict-like interface for accessing both standard
    matplotlib rcParams and custom publiplots parameters. It mimics the
    behavior of matplotlib's rcParams but includes publiplots-specific
    defaults.

    Examples
    --------
    Access parameters:
    >>> from publiplots.themes import rcParams
    >>> figsize = rcParams['figure.figsize']
    >>> color = rcParams['color']  # Custom publiplots param

    Set parameters:
    >>> rcParams['figure.figsize'] = (8, 6)
    >>> rcParams['color'] = '#ff0000'

    Use in functions with resolve_param:
    >>> from publiplots.themes.defaults import resolve_param
    >>> color = resolve_param('color', user_color)  # Uses user_color if not None
    """

    def __getitem__(self, key: str) -> Any:
        """Get parameter value."""
        return get_default(key)

    def get(self, key: str, default: Any = None) -> Any:
        """Get parameter value with optional fallback."""
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key: str, value: Any) -> None:
        """Set parameter value."""
        if key in _PUBLIPLOTS_CUSTOM_DEFAULTS:
            _PUBLIPLOTS_CUSTOM_DEFAULTS[key] = value
        else:
            plt.rcParams[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if parameter exists."""
        return key in _PUBLIPLOTS_CUSTOM_DEFAULTS or key in plt.rcParams

    def keys(self):
        """Return all parameter keys."""
        return list(_PUBLIPLOTS_CUSTOM_DEFAULTS.keys()) + list(plt.rcParams.keys())


# Create global instance
rcParams = PubliplotsRcParams()


# =============================================================================
# Parameter Resolution Functions
# =============================================================================

def get_default(key: str) -> Any:
    """
    Get a publiplots default value.

    For standard matplotlib rcParams (e.g., 'figure.figsize'), reads from plt.rcParams.
    For custom publiplots settings (e.g., 'color', 'alpha'), reads from internal defaults.

    Parameters
    ----------
    key : str
        The parameter key. Can be a full rcParam key (e.g., 'figure.figsize')
        or a custom publiplots key (e.g., 'color', 'alpha', 'palette').

    Returns
    -------
    Any
        The parameter value.

    Raises
    ------
    KeyError
        If the parameter key doesn't exist.

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
        return _PUBLIPLOTS_CUSTOM_DEFAULTS[key]

    # Otherwise, get from matplotlib rcParams
    if key in plt.rcParams:
        return plt.rcParams[key]

    # If not found anywhere, raise KeyError
    raise KeyError(f"Parameter '{key}' not found in publiplots or matplotlib rcParams")


def resolve_param(key: str, value: Optional[Any] = None) -> Any:
    """
    Resolve a parameter value: use provided value if not None, otherwise get default.

    This helper function eliminates the repetitive "if value is None: value = get_default(key)"
    pattern throughout the codebase.

    Parameters
    ----------
    key : str
        The parameter key to resolve (e.g., 'color', 'figure.figsize', 'alpha').
    value : Any, optional
        User-provided value. If None, the default will be used.

    Returns
    -------
    Any
        The resolved parameter value (user value or default).

    Examples
    --------
    Basic usage in a function:
    >>> def my_plot(color=None, figsize=None):
    ...     color = resolve_param('color', color)
    ...     figsize = resolve_param('figure.figsize', figsize)
    ...     # Now color and figsize are guaranteed to have values

    With explicit user values:
    >>> color = resolve_param('color', '#ff0000')  # Returns '#ff0000'

    With None (uses default):
    >>> color = resolve_param('color', None)  # Returns '#5d83c3'
    >>> color = resolve_param('color')  # Same as above
    """
    return value if value is not None else get_default(key)


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
    # Reset standard matplotlib rcParams
    for key, value in PUBLIPLOTS_RCPARAMS.items():
        plt.rcParams[key] = value

    # Note: Custom defaults are stored in _PUBLIPLOTS_CUSTOM_DEFAULTS
    # and don't need resetting as they're accessed by reference


def get_publiplots_rcparam(key: str) -> Any:
    """
    Get a publiplots rcParam value.

    This is a convenience function for accessing publiplots-specific
    rcParams with type safety.

    Deprecated: Use get_default() or rcParams[key] instead.

    Parameters
    ----------
    key : str
        The rcParam key to retrieve.

    Returns
    -------
    Any
        The rcParam value.

    Examples
    --------
    Get figure size:
    >>> from publiplots.themes.defaults import get_publiplots_rcparam
    >>> figsize = get_publiplots_rcparam('figure.figsize')
    >>> print(figsize)
    (3, 2)
    """
    return get_default(key)
