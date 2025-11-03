"""
Global configuration settings for prettyplot.

This module contains default settings that can be modified to change
the behavior of prettyplot functions globally.
"""

from typing import Tuple

# Default figure settings
DEFAULT_DPI: int = 300
DEFAULT_FORMAT: str = 'pdf'
DEFAULT_FIGSIZE: Tuple[float, float] = (6, 4)

# Default styling
DEFAULT_FONT: str = 'Arial'
DEFAULT_FONT_SCALE: float = 1.6
DEFAULT_STYLE: str = 'white'

# Default plot parameters
DEFAULT_LINEWIDTH: float = 2.0
DEFAULT_ALPHA: float = 0.1
DEFAULT_CAPSIZE: float = 0.0

# Color settings
DEFAULT_PALETTE: str = 'pastel_categorical'

# Hatch settings
DEFAULT_HATCH_MODE: int = 1

# Marker settings
DEFAULT_MARKER_SIZE: Tuple[float, float] = (50, 1000)
