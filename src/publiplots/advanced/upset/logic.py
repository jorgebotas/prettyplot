"""
Logic and data processing for UpSet plots.

This module handles intersection calculations, data processing, and sorting logic
for UpSet plot visualization.

Portions of this implementation are based on concepts from UpSetPlot:
https://github.com/jnothman/UpSetPlot
Copyright (c) 2016, Joel Nothman
Licensed under BSD-3-Clause
"""

from typing import Dict, List, Optional, Set, Tuple, Union
import numpy as np
import pandas as pd
from itertools import chain, combinations


def _validate_input_data(
    data: Union[pd.DataFrame, pd.Series, Dict[str, Set]]
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Validate and normalize input data to a standard format.

    Parameters
    ----------
    data : DataFrame, Series, or dict
        Input data in one of the supported formats:
        - DataFrame with MultiIndex indicating set membership (0/1)
        - DataFrame with columns as sets and boolean/binary values
        - Series with MultiIndex (first level = items, second = sets)
        - Dict mapping set names to sets of elements

    Returns
    -------
    df : DataFrame
        Normalized DataFrame with sets as columns and membership as values
    set_names : list
        List of set names in order

    Raises
    ------
    ValueError
        If data format is not recognized or invalid
    """
    if isinstance(data, dict):
        # Convert dict of sets to DataFrame
        all_elements = set(chain.from_iterable(data.values()))
        df_data = {}
        for set_name, elements in data.items():
            df_data[set_name] = [1 if elem in elements else 0 for elem in all_elements]
        df = pd.DataFrame(df_data, index=list(all_elements))
        set_names = list(data.keys())

    elif isinstance(data, pd.Series):
        # Series with MultiIndex
        if not isinstance(data.index, pd.MultiIndex):
            raise ValueError(
                "Series must have MultiIndex (items x sets) or use DataFrame format"
            )
        # Pivot to get sets as columns
        df = data.reset_index()
        if len(df.columns) < 2:
            raise ValueError("Series MultiIndex must have at least 2 levels")
        df = df.pivot_table(
            index=df.columns[0],
            columns=df.columns[1],
            values=data.name if data.name else 0,
            fill_value=0,
        )
        set_names = list(df.columns)

    elif isinstance(data, pd.DataFrame):
        # DataFrame - already in the right format
        df = data.copy()
        set_names = list(df.columns)

        # Validate values are binary (0/1 or True/False)
        unique_vals = set(df.values.flatten())
        if not unique_vals.issubset({0, 1, True, False, np.nan}):
            raise ValueError(
                "DataFrame values must be binary (0/1 or True/False) indicating set membership"
            )

    else:
        raise TypeError(
            f"Unsupported data type: {type(data)}. "
            "Use DataFrame, Series, or dict of sets."
        )

    # Ensure values are integers (0/1)
    df = df.fillna(0).astype(int)

    return df, set_names


def _calculate_intersections(
    df: pd.DataFrame,
    set_names: List[str],
    min_subset_size: Optional[int] = None,
    max_subset_size: Optional[int] = None,
    min_degree: int = 1,
    max_degree: Optional[int] = None,
) -> pd.DataFrame:
    """
    Calculate all intersections and their sizes.

    Parameters
    ----------
    df : DataFrame
        Binary membership matrix (sets as columns)
    set_names : list
        Names of sets
    min_subset_size : int, optional
        Minimum intersection size to include
    max_subset_size : int, optional
        Maximum intersection size to include
    min_degree : int, default=1
        Minimum number of sets in intersection (degree)
    max_degree : int, optional
        Maximum number of sets in intersection

    Returns
    -------
    intersections : DataFrame
        DataFrame with MultiIndex (set membership) and 'size' column
    """
    # Group by membership pattern and count
    intersection_counts = df.groupby(list(set_names)).size()

    # Filter by degree (number of sets)
    if max_degree is None:
        max_degree = len(set_names)

    def count_membership(idx):
        """Count number of sets an element belongs to."""
        return sum(idx)

    # Filter by degree
    degrees = pd.Series(
        [count_membership(idx) for idx in intersection_counts.index],
        index=intersection_counts.index
    )
    intersection_counts = intersection_counts[
        degrees.between(min_degree, max_degree)
    ]

    # Filter by subset size
    if min_subset_size is not None:
        intersection_counts = intersection_counts[intersection_counts >= min_subset_size]
    if max_subset_size is not None:
        intersection_counts = intersection_counts[intersection_counts <= max_subset_size]

    # Convert to DataFrame
    result = pd.DataFrame({"size": intersection_counts})

    return result


def _sort_intersections(
    intersections: pd.DataFrame, sort_by: str = "size", ascending: bool = False
) -> pd.DataFrame:
    """
    Sort intersections by specified criteria.

    Parameters
    ----------
    intersections : DataFrame
        Intersection data with 'size' column and MultiIndex
    sort_by : str, default='size'
        Sorting criterion:
        - 'size': Sort by intersection size
        - 'degree': Sort by number of sets (then by size)
        - 'name': Sort alphabetically by set names
    ascending : bool, default=False
        Sort order (False = descending, largest first)

    Returns
    -------
    sorted_intersections : DataFrame
        Sorted intersection data
    """
    if sort_by == "size":
        return intersections.sort_values("size", ascending=ascending)

    elif sort_by == "degree":
        # Add degree column
        intersections["degree"] = intersections.index.map(lambda x: sum(x))
        result = intersections.sort_values(
            ["degree", "size"], ascending=[ascending, ascending]
        )
        result = result.drop(columns=["degree"])
        return result

    elif sort_by == "name":
        # Sort by set membership pattern
        return intersections.sort_index()

    else:
        raise ValueError(
            f"Invalid sort_by: {sort_by}. Use 'size', 'degree', or 'name'"
        )


def _get_set_sizes(df: pd.DataFrame, set_names: List[str]) -> Dict[str, int]:
    """
    Calculate the total size of each set.

    Parameters
    ----------
    df : DataFrame
        Binary membership matrix
    set_names : list
        Names of sets

    Returns
    -------
    set_sizes : dict
        Mapping from set name to total size
    """
    return {name: int(df[name].sum()) for name in set_names}


def _prepare_plot_data(
    intersections: pd.DataFrame, set_names: List[str], show_counts: int = 20
) -> Tuple[pd.DataFrame, List[Tuple[int, ...]]]:
    """
    Prepare data for visualization.

    Parameters
    ----------
    intersections : DataFrame
        Sorted intersection data
    set_names : list
        Names of sets in order
    show_counts : int, default=20
        Maximum number of intersections to show

    Returns
    -------
    plot_data : DataFrame
        Data ready for plotting (limited to show_counts)
    membership_matrix : list of tuples
        Binary membership patterns for each intersection
    """
    # Limit to top intersections
    plot_data = intersections.head(show_counts).copy()

    # Extract membership matrix
    membership_matrix = [idx for idx in plot_data.index]

    return plot_data, membership_matrix


def process_upset_data(
    data: Union[pd.DataFrame, pd.Series, Dict[str, Set]],
    sort_by: str = "size",
    ascending: bool = False,
    min_subset_size: Optional[int] = None,
    max_subset_size: Optional[int] = None,
    min_degree: int = 1,
    max_degree: Optional[int] = None,
    show_counts: int = 20,
) -> Dict:
    """
    Process data for UpSet plot visualization.

    This is the main entry point for data processing, handling all steps from
    validation to preparation for rendering.

    Parameters
    ----------
    data : DataFrame, Series, or dict
        Input data (see _validate_input_data for formats)
    sort_by : str, default='size'
        How to sort intersections ('size', 'degree', or 'name')
    ascending : bool, default=False
        Sort order
    min_subset_size : int, optional
        Minimum intersection size to include
    max_subset_size : int, optional
        Maximum intersection size to include
    min_degree : int, default=1
        Minimum number of sets in intersection
    max_degree : int, optional
        Maximum number of sets in intersection
    show_counts : int, default=20
        Maximum number of intersections to display

    Returns
    -------
    processed : dict
        Dictionary containing:
        - 'intersections': DataFrame with intersection sizes
        - 'membership_matrix': List of membership patterns
        - 'set_names': List of set names
        - 'set_sizes': Dict of set sizes
        - 'n_sets': Number of sets
        - 'n_intersections': Number of intersections shown
    """
    # Validate and normalize input
    df, set_names = _validate_input_data(data)

    # Calculate intersections
    intersections = _calculate_intersections(
        df=df,
        set_names=set_names,
        min_subset_size=min_subset_size,
        max_subset_size=max_subset_size,
        min_degree=min_degree,
        max_degree=max_degree,
    )

    # Sort intersections
    intersections = _sort_intersections(
        intersections, sort_by=sort_by, ascending=ascending
    )

    # Get set sizes
    set_sizes = _get_set_sizes(df, set_names)

    # Prepare for plotting
    plot_data, membership_matrix = _prepare_plot_data(
        intersections, set_names, show_counts=show_counts
    )

    return {
        "intersections": plot_data,
        "membership_matrix": membership_matrix,
        "set_names": set_names,
        "set_sizes": set_sizes,
        "n_sets": len(set_names),
        "n_intersections": len(plot_data),
    }
