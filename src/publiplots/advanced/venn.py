"""
Venn diagram visualizations for publiplots.

This module provides functions for creating 2-way and 3-way Venn diagrams
with optional statistical analysis.
"""

from typing import Optional, Dict, List, Union, Tuple
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib_venn import venn2, venn2_circles, venn3, venn3_circles
from matplotlib_venn.layout.venn2 import DefaultLayoutAlgorithm as Venn2LayoutAlgorithm
from matplotlib_venn.layout.venn3 import DefaultLayoutAlgorithm as Venn3LayoutAlgorithm
from scipy.stats import hypergeom
import numpy as np
import seaborn as sns

from publiplots.config import DEFAULT_ALPHA, DEFAULT_FIGSIZE
from publiplots.themes.colors import get_palette


def venn(
    sets: Union[List[set], Dict[str, set]],
    labels: Optional[List[str]] = None,
    colors: Optional[List[str]] = None,
    universe_size: Optional[int] = None,
    weighted: bool = False,
    include_size_in_label: bool = True,
    alpha: float = DEFAULT_ALPHA,
    figsize: Tuple[float, float] = DEFAULT_FIGSIZE,
    ax: Optional[Axes] = None,
) -> Tuple[plt.Figure, Axes, Dict]:
    """
    Create a Venn diagram for 2 or 3 sets with optional overlap statistics.

    Parameters
    ----------
    sets : list of sets or dict
        Either a list of 2-3 sets, or a dictionary mapping labels to sets.
        Example: [set1, set2] or {'Group A': set1, 'Group B': set2}
    labels : list, optional
        Labels for each set. If sets is a dict, labels are taken from keys.
        Default: ['Set A', 'Set B', 'Set C']
    colors : list, optional
        Colors for each set. If None, uses pastel_categorical palette.
    universe_size : int, optional
        Total number of elements in the universe for statistical tests.
        If None, no statistical analysis is performed.
    weighted : bool, default=False
        If False, uses unweighted layout where all regions have equal area.
        If True, region sizes are proportional to set sizes.
    include_size_in_label : bool, default=True
        If True, appends set size to labels.
    alpha : float, default=0.3
        Transparency of set regions (0-1).
    figsize : tuple, default=(10, 6)
        Figure size (width, height).
    ax : Axes, optional
        Matplotlib axes object. If None, creates new figure.

    Returns
    -------
    fig : Figure
        Matplotlib figure object.
    ax : Axes
        Matplotlib axes object.
    stats : dict
        Dictionary containing overlap statistics and p-values if universe_size
        is provided.

    Examples
    --------
    Simple 2-way Venn diagram:
    >>> set1 = {1, 2, 3, 4, 5}
    >>> set2 = {4, 5, 6, 7, 8}
    >>> fig, ax, stats = pp.venn([set1, set2],
    ...                                   labels=['Group A', 'Group B'])

    3-way Venn with custom colors:
    >>> sets_dict = {'A': set1, 'B': set2, 'C': set3}
    >>> colors = pp.get_palette('pastel_categorical', n_colors=3)
    >>> fig, ax, stats = pp.venn(sets_dict, colors=colors)

    With statistical testing:
    >>> fig, ax, stats = pp.venn([set1, set2], universe_size=1000)
    >>> print(f"P-value: {stats['p_value']:.4f}")

    Notes
    -----
    - For 2-way Venn diagrams, uses hypergeometric test for overlap significance
    - For 3-way Venn diagrams, tests significance of triple intersection
    - Statistical tests require universe_size to be specified
    """
    # Parse input sets
    if isinstance(sets, dict):
        labels = list(sets.keys())
        sets = [set(s) for s in sets.values()]
    else:
        sets = [set(s) for s in sets]
        if labels is None:
            labels = [f"Set {chr(65+i)}" for i in range(len(sets))]

    # Validate number of sets
    if len(sets) not in [2, 3]:
        raise ValueError("Venn diagram supports only 2 or 3 sets")

    # Get colors
    if colors is None:
        colors = get_palette('pastel_categorical', n_colors=len(sets))

    # Set up seaborn style
    sns.set_theme("paper", style="white", font="Arial", font_scale=2)

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Decide on layout algorithm
    if not weighted:
        if len(sets) == 3:
            layout_algorithm = Venn3LayoutAlgorithm(fixed_subset_sizes=(1,) * 7)
        else:
            layout_algorithm = Venn2LayoutAlgorithm(fixed_subset_sizes=(1, 1, 1))
    else:
        layout_algorithm = None

    # Create Venn diagram based on number of sets
    if len(sets) == 2:
        stats = _create_venn2(
            sets, labels, colors, universe_size, include_size_in_label,
            alpha, layout_algorithm, weighted, ax
        )
    else:
        stats = _create_venn3(
            sets, labels, colors, universe_size, include_size_in_label,
            alpha, layout_algorithm, weighted, ax
        )

    plt.tight_layout()
    return fig, ax, stats


def _create_venn2(
    sets: List[set],
    labels: List[str],
    colors: List[str],
    universe_size: Optional[int],
    include_size_in_label: bool,
    alpha: float,
    layout_algorithm,
    weighted: bool,
    ax: Axes
) -> Dict:
    """Create 2-way Venn diagram."""
    A, B = sets
    labelA, labelB = labels[:2]
    colorA, colorB = colors[:2]

    if include_size_in_label:
        labelA, labelB = f"{labelA} ({len(A)})", f"{labelB} ({len(B)})"

    size_A = len(A)
    size_B = len(B)
    overlap = len(A.intersection(B))

    # Prepare data for venn2
    subsets = (size_A - overlap, size_B - overlap, overlap)

    # Create Venn diagram
    v = venn2(
        subsets=subsets,
        set_labels=(labelA, labelB),
        set_colors=(colorA, colorB),
        layout_algorithm=layout_algorithm,
        ax=ax
    )

    # Increase transparency
    for patch in v.patches:
        if patch is not None:
            patch.set_alpha(alpha)

    # Add circles for clarity
    circles = venn2_circles(
        subsets=subsets if weighted else [1, 1, 1],
        linestyle="solid",
        linewidth=2,
        color="black",
        layout_algorithm=layout_algorithm,
        ax=ax
    )

    # Override circle edge colors
    for i, color in enumerate([colorA, colorB]):
        if circles[i] is not None:
            circles[i].set_edgecolor(color)

    # Statistical test if universe_size provided
    if universe_size is None:
        return {
            "set_sizes": [size_A, size_B],
            "overlap": overlap,
            "expected_overlap": None,
            "fold_enrichment": None,
            "log2_fold_enrichment": None,
            "p_value": None,
            "significant": None
        }

    # Hypergeometric test for overlap
    p_value = hypergeom.sf(overlap - 1, universe_size, size_A, size_B)
    expected_overlap = (size_A * size_B) / universe_size
    fold_enrichment = overlap / expected_overlap if expected_overlap > 0 else float("inf")
    log2_fold_enrichment = np.log2(fold_enrichment) if fold_enrichment > 0 else float("inf")

    # Show stats
    ax.text(
        0.5, -0.12,
        f"P-value: {p_value:.2e}",
        horizontalalignment="center",
        transform=ax.transAxes
    )
    ax.text(
        0.5, -0.17,
        f"Expected overlap: {expected_overlap:.2f}, "
        f"Fold enrichment: {fold_enrichment:.2f}x (log2: {log2_fold_enrichment:.2f})",
        horizontalalignment="center",
        transform=ax.transAxes,
    )

    return {
        "set_sizes": [size_A, size_B],
        "overlap": overlap,
        "expected_overlap": expected_overlap,
        "fold_enrichment": fold_enrichment,
        "log2_fold_enrichment": log2_fold_enrichment,
        "p_value": p_value,
        "significant": p_value < 0.05
    }


def _create_venn3(
    sets: List[set],
    labels: List[str],
    colors: List[str],
    universe_size: Optional[int],
    include_size_in_label: bool,
    alpha: float,
    layout_algorithm,
    weighted: bool,
    ax: Axes
) -> Dict:
    """Create 3-way Venn diagram."""
    A, B, C = sets
    labelA, labelB, labelC = labels[:3]
    colorA, colorB, colorC = colors[:3]

    if include_size_in_label:
        labelA = f"{labelA} ({len(A)})"
        labelB = f"{labelB} ({len(B)})"
        labelC = f"{labelC} ({len(C)})"

    # Compute all subset sizes for 3-set Venn
    onlyA = len(A - B - C)
    onlyB = len(B - A - C)
    onlyC = len(C - A - B)
    AB_only = len((A & B) - C)
    AC_only = len((A & C) - B)
    BC_only = len((B & C) - A)
    ABC = len(A & B & C)

    size_A = len(A)
    size_B = len(B)
    size_C = len(C)

    # Prepare data for venn3
    subsets = (onlyA, onlyB, AB_only, onlyC, AC_only, BC_only, ABC)

    # Create Venn diagram
    v = venn3(
        subsets=subsets,
        set_labels=(labelA, labelB, labelC),
        set_colors=(colorA, colorB, colorC),
        layout_algorithm=layout_algorithm,
        ax=ax
    )

    # Increase transparency
    for patch in v.patches:
        if patch is not None:
            patch.set_alpha(alpha)

    # Add circles
    circles = venn3_circles(
        subsets=subsets if weighted else [1]*7,
        linestyle="solid",
        linewidth=2,
        color="black",
        layout_algorithm=layout_algorithm,
        ax=ax
    )

    # Override circle edge colors
    for i, color in enumerate([colorA, colorB, colorC]):
        if circles[i] is not None:
            circles[i].set_edgecolor(color)

    if universe_size is None:
        return {
            "set_sizes": [size_A, size_B, size_C],
            "unique_counts": {
                f"{labelA} only": onlyA,
                f"{labelB} only": onlyB,
                f"{labelC} only": onlyC
            },
            "pairwise_overlaps": {
                f"{labelA}&{labelB} only": AB_only,
                f"{labelA}&{labelC} only": AC_only,
                f"{labelB}&{labelC} only": BC_only
            },
            "triple_overlap": ABC,
            "expected_triple_overlap": None,
            "fold_enrichment": None,
            "log2_fold_enrichment": None,
            "p_value": None,
            "significant": None
        }

    # Hypergeometric test on triple intersection
    BC = B & C
    size_BC = len(BC)
    p_value = hypergeom.sf(ABC - 1, universe_size, size_A, size_BC)

    # Expected triple intersection
    expected_abc = (size_A * size_B * size_C) / (universe_size**2)
    fold_enrichment = (ABC / expected_abc) if expected_abc > 0 else float("inf")
    log2_fold_enrichment = np.log2(fold_enrichment) if fold_enrichment > 0 else float("inf")

    # Show p-value and enrichment
    ax.text(
        0.5, -0.10,
        f"P-value (for triple intersection): {p_value:.2e}",
        horizontalalignment="center",
        transform=ax.transAxes
    )
    ax.text(
        0.5, -0.15,
        f"Expected triple intersection: {expected_abc:.2f}, "
        f"Fold enrichment: {fold_enrichment:.2f}x (log2: {log2_fold_enrichment:.2f})",
        horizontalalignment="center",
        transform=ax.transAxes,
    )

    return {
        "set_sizes": [size_A, size_B, size_C],
        "unique_counts": {
            f"{labelA} only": onlyA,
            f"{labelB} only": onlyB,
            f"{labelC} only": onlyC
        },
        "pairwise_overlaps": {
            f"{labelA}&{labelB} only": AB_only,
            f"{labelA}&{labelC} only": AC_only,
            f"{labelB}&{labelC} only": BC_only
        },
        "triple_overlap": ABC,
        "expected_triple_overlap": expected_abc,
        "fold_enrichment": fold_enrichment,
        "log2_fold_enrichment": log2_fold_enrichment,
        "p_value": p_value,
        "significant": p_value < 0.05
    }
