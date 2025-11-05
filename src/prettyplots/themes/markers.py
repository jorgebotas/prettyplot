"""
Marker definitions and utilities for prettyplots.

This module provides standard marker sets and utilities for consistent
marker usage across visualizations.
"""

from typing import List, Dict, Tuple


# =============================================================================
# Marker Sets
# =============================================================================

STANDARD_MARKERS: List[str] = [
    'o',   # Circle
    's',   # Square
    '^',   # Triangle up
    'D',   # Diamond
    'v',   # Triangle down
    'p',   # Pentagon
    '*',   # Star
    'h',   # Hexagon
    '<',   # Triangle left
    '>',   # Triangle right
]
"""
Standard set of distinguishable markers for categorical data.

Use case: When plotting multiple categories in scatter plots or line plots
where shape needs to distinguish groups in addition to or instead of color.

Example:
    >>> import prettyplots as pp
    >>> markers = pp.STANDARD_MARKERS
    >>> for i, category in enumerate(categories):
    ...     pp.scatterplot(data[data.cat==category], marker=markers[i])
"""

SIMPLE_MARKERS: List[str] = [
    'o',   # Circle
    's',   # Square
    '^',   # Triangle up
    'D',   # Diamond
]
"""
Simple marker set with 4 easily distinguishable shapes.

Use case: When only a few categories need to be represented, these
provide maximum clarity and are easily distinguishable even at small sizes.
"""

FILLED_UNFILLED_MARKERS: Dict[str, Tuple[str, str]] = {
    "circle": ('o', 'o'),          # Circle (same filled/unfilled)
    "square": ('s', 's'),          # Square
    "triangle_up": ('^', '^'),     # Triangle up
    "triangle_down": ('v', 'v'),   # Triangle down
    "diamond": ('D', 'd'),         # Diamond (filled, unfilled)
    "pentagon": ('p', 'p'),        # Pentagon
    "hexagon": ('h', 'h'),         # Hexagon
    "star": ('*', '*'),            # Star
}
"""
Mapping of marker names to (filled, unfilled) marker codes.

Use case: When you want to use the same shape but distinguish groups
by fill status (e.g., treatment vs control).

Example:
    >>> markers = pp.FILLED_UNFILLED_MARKERS
    >>> pp.scatterplot(treated, marker=markers['circle'][0])   # Filled
    >>> pp.scatterplot(control, marker=markers['circle'][1])   # Unfilled
"""


# =============================================================================
# Marker Size Recommendations
# =============================================================================

MARKER_SIZES: Dict[str, float] = {
    "small": 20,
    "medium": 50,
    "large": 100,
    "xlarge": 200,
}
"""
Recommended marker sizes for scatter plots (in points^2).

Use case: Provides consistent sizing across plots. These sizes are
calibrated to work well with prettyplots's default styling.

Example:
    >>> pp.scatterplot(data, x='x', y='y', s=pp.MARKER_SIZES['medium'])
"""

SIZE_RANGE_CATEGORICAL: Tuple[float, float] = (50, 200)
"""
Recommended size range for categorical data with size encoding.

Use case: When size represents discrete categories (e.g., small/medium/large).
"""

SIZE_RANGE_CONTINUOUS: Tuple[float, float] = (50, 1000)
"""
Recommended size range for continuous data with size encoding.

Use case: When size represents a continuous variable (e.g., p-value, effect size).
This range provides good visual distinction without markers becoming too large.
"""


# =============================================================================
# Hatch Patterns
# =============================================================================

HATCH_PATTERNS: List[str] = [
    '',        # No hatch
    '///',     # Diagonal lines (forward)
    '\\\\\\',  # Diagonal lines (backward)
    '|||',     # Vertical lines
    '---',     # Horizontal lines
    '+++',     # Plus signs
    'xxx',     # Crosses
    '...',     # Dots
]
"""
Standard hatch patterns for bar plots and patches.

Use case: When color alone is insufficient (e.g., for colorblind accessibility
or black-and-white printing), hatch patterns provide an additional visual
encoding dimension.

Example:
    >>> import prettyplots as pp
    >>> hatches = pp.HATCH_PATTERNS
    >>> pp.barplot(data, x='group', y='value', hatch=hatches[1])
"""


# =============================================================================
# Functions
# =============================================================================

def get_marker_cycle(n: int, style: str = "standard") -> List[str]:
    """
    Get a cycle of n markers from a predefined style.

    Parameters
    ----------
    n : int
        Number of markers needed.
    style : str, default='standard'
        Marker style: 'standard' or 'simple'.

    Returns
    -------
    List[str]
        List of n marker codes. If n exceeds available markers,
        cycles through the list.

    Examples
    --------
    >>> markers = get_marker_cycle(5, style='standard')
    >>> len(markers)
    5
    """
    if style == "standard":
        marker_set = STANDARD_MARKERS
    elif style == "simple":
        marker_set = SIMPLE_MARKERS
    else:
        raise ValueError(f"Unknown marker style '{style}'. Use 'standard' or 'simple'.")

    # Cycle through markers if n exceeds available markers
    return [marker_set[i % len(marker_set)] for i in range(n)]


def get_hatch_cycle(n: int) -> List[str]:
    """
    Get a cycle of n hatch patterns.

    Parameters
    ----------
    n : int
        Number of hatch patterns needed.

    Returns
    -------
    List[str]
        List of n hatch pattern strings.

    Examples
    --------
    >>> hatches = get_hatch_cycle(5)
    >>> len(hatches)
    5
    """
    return [HATCH_PATTERNS[i % len(HATCH_PATTERNS)] for i in range(n)]


def get_size_mapping(
    values: List[float],
    size_range: Tuple[float, float] = SIZE_RANGE_CONTINUOUS,
    method: str = "linear"
) -> List[float]:
    """
    Map data values to marker sizes.

    Parameters
    ----------
    values : List[float]
        Data values to map.
    size_range : Tuple[float, float], default=SIZE_RANGE_CONTINUOUS
        (min_size, max_size) in points^2.
    method : str, default='linear'
        Mapping method: 'linear' or 'log'.

    Returns
    -------
    List[float]
        Mapped marker sizes.

    Examples
    --------
    Map p-values to sizes:
    >>> pvalues = [0.001, 0.01, 0.05, 0.1]
    >>> neg_log_p = [-np.log10(p) for p in pvalues]
    >>> sizes = get_size_mapping(neg_log_p, size_range=(50, 500))
    """
    import numpy as np

    values = np.array(values)
    min_size, max_size = size_range

    if method == "linear":
        # Linear scaling
        v_min, v_max = values.min(), values.max()
        if v_max == v_min:
            return [min_size] * len(values)
        normalized = (values - v_min) / (v_max - v_min)
        sizes = min_size + normalized * (max_size - min_size)

    elif method == "log":
        # Log scaling
        log_values = np.log10(values + 1)  # Add 1 to avoid log(0)
        v_min, v_max = log_values.min(), log_values.max()
        if v_max == v_min:
            return [min_size] * len(values)
        normalized = (log_values - v_min) / (v_max - v_min)
        sizes = min_size + normalized * (max_size - min_size)

    else:
        raise ValueError(f"Unknown method '{method}'. Use 'linear' or 'log'.")

    return sizes.tolist()
