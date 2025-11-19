"""
Marker definitions and utilities for publiplots.

This module provides standard marker sets and utilities for consistent
marker usage across visualizations.
"""

from typing import List, Dict, Tuple, Optional, Union


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
    >>> import publiplots as pp
    >>> markers = pp.STANDARD_MARKERS
    >>> for i, category in enumerate(categories):
    ...     pp.scatterplot(data[data.cat==category], marker=markers[i])
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
calibrated to work well with publiplots's default styling.

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
# Functions
# =============================================================================

def resolve_markers(
    markers: Optional[List[str]] = None,
    n_markers: Optional[int] = None,
    reverse: bool = False,
    style: str = "standard"
) -> List[str]:
    """
    Resolve marker patterns for plotting.

    This is a helper function that standardizes marker specifications
    into a concrete list of markers. It handles marker cycling for arbitrary
    numbers of categories and supports marker reversal.

    Parameters
    ----------
    markers : list of str, optional
        List of marker symbols to use. If None, uses default markers from
        STANDARD_MARKERS or SIMPLE_MARKERS based on the style parameter.
    n_markers : int, optional
        Number of markers to return. If provided, markers will be
        cycled to reach this count. If None, returns all markers.
    reverse : bool, default=False
        Whether to reverse the marker order. Useful for changing visual
        hierarchy.
    style : str, default='standard'
        Marker style: 'standard' or 'simple'. Only applicable when markers is None.

    Returns
    -------
    List[str]
        List of resolved marker symbols.

    Examples
    --------
    Get default markers:
    >>> markers = resolve_markers()
    >>> len(markers)
    10

    Get exactly 5 markers with cycling:
    >>> markers = resolve_markers(n_markers=5)
    >>> len(markers)
    5

    Use custom markers:
    >>> markers = resolve_markers(markers=['o', '^', 's'], n_markers=7)

    Get reversed markers:
    >>> markers = resolve_markers(n_markers=4, reverse=True)

    Use simple style:
    >>> markers = resolve_markers(n_markers=5, style='simple')

    See Also
    --------
    resolve_marker_map : Create a mapping from values to markers
    get_marker_cycle : Get a cycle of n markers
    """
    # Get default markers if not provided
    if markers is None:
        if style == "standard":
            markers = STANDARD_MARKERS
        elif style == "simple":
            markers = STANDARD_MARKERS[:4]  # First 4 markers for simple style
        else:
            raise ValueError(f"Unknown marker style '{style}'. Use 'standard' or 'simple'.")

    # Cycle markers if n_markers specified
    if n_markers is not None:
        markers = [markers[i % len(markers)] for i in range(n_markers)]

    # Reverse if requested
    if reverse:
        markers = markers[::-1]

    return markers


def resolve_marker_map(
    values: Optional[List[str]] = None,
    marker_map: Optional[Union[Dict[str, str], List[str]]] = None,
    reverse: bool = False,
    style: str = "standard"
) -> Dict[str, str]:
    """
    Create a mapping from category values to marker symbols.

    This function creates a dictionary that maps category names to specific
    marker symbols, which is useful for categorical plots like scatterplots
    with style parameter. It ensures consistent marker assignment across
    multiple plots.

    Parameters
    ----------
    values : list of str, optional
        List of category values to map to markers. If None, returns empty dict.
    marker_map : dict or list, optional
        Marker specification:
        - dict: Explicit mapping from values to markers (returned as-is)
        - list: List of markers to cycle through for values
        - None: Uses default markers from STANDARD_MARKERS
    reverse : bool, default=False
        Whether to reverse the marker assignment order. Only applicable
        when marker_map is a list or None.
    style : str, default='standard'
        Marker style: 'standard' or 'simple'. Only applicable when
        marker_map is None.

    Returns
    -------
    Dict[str, str]
        Mapping from category values to marker symbols.

    Examples
    --------
    Create mapping for categories:
    >>> categories = ['A', 'B', 'C', 'D']
    >>> mapping = resolve_marker_map(values=categories)
    >>> mapping['A']
    'o'
    >>> mapping['B']
    's'

    Use custom markers:
    >>> mapping = resolve_marker_map(
    ...     values=['cat', 'dog', 'bird'],
    ...     marker_map=['o', '^', 's']
    ... )

    Use explicit mapping:
    >>> mapping = resolve_marker_map(
    ...     values=['A', 'B'],
    ...     marker_map={'A': 'o', 'B': '^'}
    ... )
    >>> mapping
    {'A': 'o', 'B': '^'}

    Use simple style:
    >>> mapping = resolve_marker_map(values=['A', 'B', 'C'], style='simple')

    See Also
    --------
    resolve_markers : Resolve markers without creating a mapping
    get_marker_cycle : Get a cycle of n markers
    """
    # Return empty dict if no values provided
    if values is None:
        return {}

    # If already a dict, return as-is
    if isinstance(marker_map, dict):
        return marker_map

    # Resolve markers and create mapping
    markers = resolve_markers(
        markers=marker_map,
        n_markers=len(values),
        reverse=reverse,
        style=style
    )

    return {value: marker for value, marker in zip(values, markers)}


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
