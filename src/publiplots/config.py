"""
Global configuration settings for publiplots.

.. deprecated::
    This module is deprecated and will be removed in a future version.
    publiplots now uses matplotlib's rcParams for all configuration.

    All settings are now managed through matplotlib's rcParams system:
    - Standard matplotlib params: figure.figsize, savefig.dpi, lines.linewidth, etc.
    - Custom publiplots params: via get_default('color'), get_default('alpha'), etc.

    To customize defaults:
    1. Use style functions:
       - pp.set_notebook_style() - For interactive work (larger figures, readable fonts)
       - pp.set_publication_style() - For final figures (compact, high DPI, Illustrator-ready)
    2. Modify rcParams directly: plt.rcParams["figure.figsize"] = (8, 6)
    3. Use from publiplots.themes.rcparams import get_default, reset_to_publiplots_defaults()
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
DEFAULT_PALETTE: str = 'pastel'

# Hatch settings
DEFAULT_HATCH_MODE: int = 1