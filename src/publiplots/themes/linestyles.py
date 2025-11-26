"""
Line style definitions and utilities for publiplots.

This module provides standard line style sets and utilities for consistent
line style usage across visualizations. Line styles are particularly useful
for distinguishing multiple lines in line plots, time series, or when color
alone is insufficient (e.g., black-and-white printing).
"""

from typing import List, Dict, Tuple, Optional, Union
from publiplots.themes.rcparams import resolve_param


# =============================================================================
# Line Style Sets
# =============================================================================

STANDARD_LINESTYLES: List[str] = [
    '-',      # Solid line
    '--',     # Dashed line
    '-.',     # Dash-dot line
    ':',      # Dotted line
]
"""
Standard set of matplotlib line styles.

Use case: Basic line style cycling for line plots where different line
styles need to distinguish groups.

"""



# =============================================================================
# Functions
# =============================================================================

def resolve_linestyles(
    linestyles: Optional[List[Union[str, Tuple]]] = None,
    n_linestyles: Optional[int] = None,
    reverse: bool = False,
) -> List[Union[str, Tuple]]:
    """
    Resolve line style patterns for plotting.

    This is a helper function that standardizes line style specifications
    into a concrete list of line styles. It handles line style cycling for
    arbitrary numbers of lines and supports line style reversal.

    Parameters
    ----------
    linestyles : list of str or tuple, optional
        List of line style patterns to use. If None, uses default line styles
        from STANDARD_LINESTYLES.
    n_linestyles : int, optional
        Number of line styles to return. If provided, line styles will be
        cycled to reach this count. If None, returns all line styles.
    reverse : bool, default=False
        Whether to reverse the line style order. Useful for changing visual
        hierarchy.

    Returns
    -------
    List[Union[str, Tuple]]
        List of resolved line style patterns.

    Examples
    --------
    Get default line styles:
    >>> linestyles = resolve_linestyles()
    >>> len(linestyles)
    4

    Get exactly 5 line styles with cycling:
    >>> linestyles = resolve_linestyles(n_linestyles=5)
    >>> len(linestyles)
    5

    Use custom line styles:
    >>> linestyles = resolve_linestyles(linestyles=['-', '--', '-.'], n_linestyles=7)

    Get reversed line styles:
    >>> linestyles = resolve_linestyles(n_linestyles=4, reverse=True)

    See Also
    --------
    resolve_linestyle_map : Create a mapping from values to line styles
    """
    # Get default line styles if not provided
    if linestyles is None:
        linestyles = STANDARD_LINESTYLES

    # Cycle line styles if n_linestyles specified
    if n_linestyles is not None:
        linestyles = [linestyles[i % len(linestyles)] for i in range(n_linestyles)]

    # Reverse if requested
    if reverse:
        linestyles = linestyles[::-1]

    return linestyles


def resolve_linestyle_map(
    values: Optional[List[str]] = None,
    linestyle_map: Optional[Union[Dict[str, Union[str, Tuple]], List[Union[str, Tuple]]]] = None,
    reverse: bool = False,
) -> Dict[str, Union[str, Tuple]]:
    """
    Create a mapping from category values to line styles.

    This function creates a dictionary that maps category names to specific
    line styles, which is useful for categorical line plots. It ensures
    consistent line style assignment across multiple plots.

    Parameters
    ----------
    values : list of str, optional
        List of category values to map to line styles. If None, returns empty dict.
    linestyle_map : dict or list, optional
        Line style specification:
        - dict: Explicit mapping from values to line styles (returned as-is)
        - list: List of line styles to cycle through for values
        - None: Uses default line styles from STANDARD_LINESTYLES
    reverse : bool, default=False
        Whether to reverse the line style assignment order. Only applicable
        when linestyle_map is a list or None.

    Returns
    -------
    Dict[str, Union[str, Tuple]]
        Mapping from category values to line style patterns.

    Examples
    --------
    Create mapping for categories:
    >>> categories = ['A', 'B', 'C', 'D']
    >>> mapping = resolve_linestyle_map(values=categories)
    >>> mapping['A']
    '-'
    >>> mapping['B']
    '--'

    Use custom line styles:
    >>> mapping = resolve_linestyle_map(
    ...     values=['control', 'treatment', 'placebo'],
    ...     linestyle_map=['-', '--', '-.']
    ... )

    Use explicit mapping:
    >>> mapping = resolve_linestyle_map(
    ...     values=['A', 'B'],
    ...     linestyle_map={'A': '-', 'B': '--'}
    ... )
    >>> mapping
    {'A': '-', 'B': '--'}

    See Also
    --------
    resolve_linestyles : Resolve line styles without creating a mapping
    """
    # Return empty dict if no values provided
    if values is None:
        return {}

    # If already a dict, return as-is
    if isinstance(linestyle_map, dict):
        return linestyle_map

    # Resolve line styles and create mapping
    linestyles = resolve_linestyles(
        linestyles=linestyle_map,
        n_linestyles=len(values),
        reverse=reverse,
    )

    return {value: linestyle for value, linestyle in zip(values, linestyles)}