import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3, venn3_circles
from matplotlib_venn.layout.venn2 import DefaultLayoutAlgorithm as Venn2LayoutAlgorithm
from matplotlib_venn.layout.venn3 import DefaultLayoutAlgorithm as Venn3LayoutAlgorithm
from scipy.stats import hypergeom
import numpy as np
from typing import Optional

def gene_overlap(
    sets: list, 
    labels: list = ["Set A", "Set B", "Set C"], 
    colors: list = ["#75b375", "#8e8ec1", "#eeaa58"],
    universe_size: Optional[int] = None,
    weighted: bool = False,
    include_size_in_label: bool = True,
    alpha: float = 0.3,
    save: Optional[str] = None
):
    """
    Analyze overlap between two or three gene sets, create a Venn diagram, and compute significance.
    
    Parameters
    ----------
    sets : list
        A list of 2 or 3 sets of genes
    labels : list
        A list of labels corresponding to each set
    colors : list
        A list of color hex codes or valid matplotlib color strings (length 2 or 3)
    universe_size : int
        Total number of genes in the universe
    weighted : bool, default=True
        If False, uses "unweighted" layout with all subset areas forced equal (for 2-set Venn).
        For a 3-set Venn, it is similarly forced using DefaultLayoutAlgorithm with fixed subset sizes.
    include_size_in_label : bool, default=True
        If True, appends the size of each set to its label.
        If False, only the label is shown.
        
    Returns
    -------
    dict
        Dictionary containing:
            - set sizes
            - overlap(s)
            - expected overlap(s)
            - fold enrichment
            - log2 fold enrichment
            - hypergeometric p-value
            - significance (p_value < 0.05)
    """
    sns.set_theme("paper", style="white", font="Arial", font_scale=2)
    
    # Basic checks
    if len(sets) not in [2, 3]:
        raise ValueError("This function only handles 2 or 3 sets.")
        
    # Convert items in sets to Python sets if they aren"t already
    sets = [set(s) for s in sets]
    
    # Decide on layout
    if not weighted:
        # Force subset sizes to be the same in the layout by passing in fixed_subset_sizes
        # (or None if we just want default for 3-venn).
        layout_algorithm = Venn3LayoutAlgorithm(
            fixed_subset_sizes=(1,) * 7
        ) if len(sets) == 3 else Venn2LayoutAlgorithm(
            fixed_subset_sizes=(1, 1, 1)
        )
    else:
        layout_algorithm = None
    
    # -------- 2-SET CASE --------
    if len(sets) == 2:
        A, B = sets
        labelA, labelB = list(labels)[:2]
        if include_size_in_label:
            labelA, labelB = (
                f"{labelA} ({len(A)})", 
                f"{labelB} ({len(B)})"
            )
        colorA, colorB = list(colors)[:2]
        
        size_A = len(A)
        size_B = len(B)
        overlap = len(A.intersection(B))
        
        # Prepare data for venn2
        subsets = (size_A - overlap, 
                   size_B - overlap, 
                   overlap)
        
        plt.figure(figsize=(10, 6))
        v = venn2(
            subsets=subsets,
            set_labels=(labelA, labelB),
            set_colors=(colorA, colorB),
            layout_algorithm=layout_algorithm
        )
        
        # Increase transparency
        for patch in v.patches:
            if patch is not None:
                patch.set_alpha(alpha)
        
        # Add dashed circles for clarity
        circles = venn2_circles(
            subsets=subsets if weighted else [1, 1, 1],
            linestyle="solid", 
            linewidth=2,
            color="black",
            layout_algorithm=layout_algorithm
        )

        # Override circle edge colors manually
        for i, color in enumerate([colorA, colorB]):
            if circles[i] is not None:
                circles[i].set_edgecolor(color)

        
        if universe_size is None:
            plt.tight_layout()

            if save:
                plt.savefig(
                    save, 
                    dpi=600, 
                    transparent=True, 
                    bbox_inches="tight"
                )

            plt.show()
            return {
                "set_sizes": [size_A, size_B],
                "overlap": overlap,
                "expected_overlap": None,
                "fold_enrichment": None,
                "log2_fold_enrichment": None,
                "p_value": None,
                "significant": None
            }
        
        # Hypergeometric test for overlap of two sets
        p_value = hypergeom.sf(overlap - 1, universe_size, size_A, size_B)
        
        expected_overlap = (size_A * size_B) / universe_size
        fold_enrichment = overlap / expected_overlap if expected_overlap > 0 else float("inf")
        log2_fold_enrichment = np.log2(fold_enrichment) if fold_enrichment > 0 else float("inf")
        
        # Show stats
        plt.text(
            0.5, -0.12, 
            f"P-value: {p_value:.2e}",
            horizontalalignment="center", 
            transform=plt.gca().transAxes
        )
        plt.text(
            0.5, -0.17, 
            f"Expected overlap: {expected_overlap:.2f}, "
            f"Fold enrichment: {fold_enrichment:.2f}x (log2: {log2_fold_enrichment:.2f})",
            horizontalalignment="center", 
            transform=plt.gca().transAxes, 
        )
        
        plt.tight_layout()

        if save:
            plt.savefig(
                save, 
                dpi=600, 
                transparent=True, 
                bbox_inches="tight"
            )

        plt.show()
        
        return {
            "set_sizes": [size_A, size_B],
            "overlap": overlap,
            "expected_overlap": expected_overlap,
            "fold_enrichment": fold_enrichment,
            "log2_fold_enrichment": log2_fold_enrichment,
            "p_value": p_value,
            "significant": p_value < 0.05
        }
    
    # -------- 3-SET CASE --------
    else:
        A, B, C = sets
        labelA, labelB, labelC = labels
        if include_size_in_label:
            labelA, labelB, labelC = (
                f"{labelA} ({len(A)})", 
                f"{labelB} ({len(B)})", 
                f"{labelC} ({len(C)})"
            )
        colorA, colorB, colorC = colors
        
        # Compute all subset sizes for 3-set Venn:
        # A only, B only, C only
        onlyA  = len(A - B - C)
        onlyB  = len(B - A - C)
        onlyC  = len(C - A - B)
        # pairwise intersections only
        AB_only = len((A & B) - C)
        AC_only = len((A & C) - B)
        BC_only = len((B & C) - A)
        # triple intersection
        ABC     = len(A & B & C)
        
        # Summaries
        size_A = len(A)
        size_B = len(B)
        size_C = len(C)
        
        # Prepare data for venn3
        subsets = (
            onlyA, 
            onlyB, 
            AB_only, 
            onlyC, 
            AC_only, 
            BC_only, 
            ABC
        )
        
        plt.figure(figsize=(10, 6))
        
        v = venn3(
            subsets=subsets,
            set_labels=(labelA, labelB, labelC),
            set_colors=(colorA, colorB, colorC),
            layout_algorithm=layout_algorithm
        )
        
        # Increase transparency
        for patch in v.patches:
            if patch is not None:
                patch.set_alpha(alpha)
        
        # Add dashed circles
        circles = venn3_circles(
            subsets=subsets if weighted else [1]*7,
            linestyle="solid",
            linewidth=2,
            color="black",
            layout_algorithm=layout_algorithm
        )

        # Override circle edge colors manually
        for i, color in enumerate([colorA, colorB, colorC]):
            if circles[i] is not None:
                circles[i].set_edgecolor(color)

        if universe_size is None:
            plt.tight_layout()
            if save:
                plt.savefig(
                    save, 
                    dpi=600, 
                    transparent=True, 
                    bbox_inches="tight"
                )
            plt.show()
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
        
        # Hypergeometric test on triple intersection by combining B∩C as a single set
        BC = B & C
        size_BC = len(BC)
        
        # Probability that A intersects with B∩C at least ABC times
        p_value = hypergeom.sf(ABC - 1, universe_size, size_A, size_BC)
        
        # Expected triple intersection if memberships were random and independent:
        # ~ (|A| * |B| * |C|) / (universe_size^2) in an approximate sense
        expected_abc = (size_A * size_B * size_C) / (universe_size**2)
        fold_enrichment = (ABC / expected_abc) if expected_abc > 0 else float("inf")
        log2_fold_enrichment = np.log2(fold_enrichment) if fold_enrichment > 0 else float("inf")
        
        # Show p-value and enrichment for triple overlap
        plt.text(
            0.5, -0.10, 
            f"P-value (for triple intersection): {p_value:.2e}",
            horizontalalignment="center", 
            transform=plt.gca().transAxes
        )
        plt.text(
            0.5, -0.15,
            f"Expected triple intersection: {expected_abc:.2f}, "
            f"Fold enrichment: {fold_enrichment:.2f}x (log2: {log2_fold_enrichment:.2f})", 
            horizontalalignment="center", 
            transform=plt.gca().transAxes, 
        )
        
        plt.tight_layout()

        if save:
            plt.savefig(
                save, 
                dpi=600, 
                transparent=True, 
                bbox_inches="tight"
            )

        plt.show()
        
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