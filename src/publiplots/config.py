"""
Global configuration settings for publiplots.

.. deprecated::
    This module is deprecated and will be removed in a future version.
    publiplots now uses matplotlib's rcParams for all configuration.

    All default values are now read from rcParams:
    - DEFAULT_FIGSIZE -> plt.rcParams["figure.figsize"]
    - DEFAULT_DPI -> plt.rcParams["savefig.dpi"]
    - DEFAULT_FORMAT -> plt.rcParams["savefig.format"]
    - DEFAULT_LINEWIDTH -> plt.rcParams["lines.linewidth"]
    - DEFAULT_ALPHA -> plt.rcParams["publiplots.alpha"]
    - DEFAULT_CAPSIZE -> plt.rcParams["publiplots.capsize"]
    - DEFAULT_COLOR -> plt.rcParams["publiplots.color"]
    - DEFAULT_PALETTE -> plt.rcParams["publiplots.palette"]
    - DEFAULT_HATCH_MODE -> plt.rcParams["publiplots.hatch_mode"]

    To customize defaults, either:
    1. Use style functions: pp.set_notebook_style() or pp.set_publication_style()
    2. Modify rcParams directly: plt.rcParams["figure.figsize"] = (8, 6)
    3. Use publiplots.themes.defaults.reset_to_publiplots_defaults()
"""

import warnings
warnings.warn(
    "publiplots.config is deprecated and will be removed in a future version. "
    "Use matplotlib's rcParams instead. See module docstring for details.",
    DeprecationWarning,
    stacklevel=2
)

from typing import Tuple

# Default figure settings
DEFAULT_DPI: int = 300
DEFAULT_FORMAT: str = 'pdf'
DEFAULT_FIGSIZE: Tuple[float, float] = (3, 2)

# Default styling
DEFAULT_FONT: str = 'Arial'
DEFAULT_FONT_SCALE: float = 1.6
DEFAULT_STYLE: str = 'white'
DEFAULT_COLOR: str = '#5d83c3' # slate blue

# Default plot parameters
DEFAULT_LINEWIDTH: float = 1.0
DEFAULT_ALPHA: float = 0.1
DEFAULT_CAPSIZE: float = 0.0

# Color settings
DEFAULT_PALETTE: str = 'pastel_categorical'

# Hatch settings
DEFAULT_HATCH_MODE: int = 1