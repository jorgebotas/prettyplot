from typing import Optional, Dict, List
HATCH_PATTERNS: List[str] = [
   "",        # No hatch
    "///",     # Diagonal lines (forward)
    "\\\\\\",  # Diagonal lines (backward)
    "...",     # Dots
    "|||",     # Vertical lines
    "---",     # Horizontal lines
    "+++",     # Plus signs
    "xxx",     # Crosses
]


def resolve_hatches(
        hatches: Optional[List[str]] = None,
        n_hatches: Optional[int] = None,
        reverse: bool = False
    ) -> List[str]:
    """
    Resolve a hatch mapping to actual hatch patterns.

    Parameters
    ----------
    hatches : list, optional
        List of hatch patterns.
    n_hatches : int, optional
    """

    if hatches is None:
        hatches = HATCH_PATTERNS

    if n_hatches is not None:
        hatches = [ hatches[i % len(hatches)] for i in range(n_hatches) ]

    if reverse:
        hatches = hatches[::-1]

    return hatches

def resolve_hatch_mapping(
        values: Optional[List[str]] = None,
        hatch_mapping: Optional[Dict[str, str]] = None,
        reverse: bool = False
    ) -> Dict[str, str]:
    """
    Resolve a hatch mapping to actual hatch patterns.

    Parameters
    ----------
    values : list
        List of values to resolve hatch patterns for.
    hatch_mapping : dict, optional
        Mapping from hatch values to hatch patterns.
    reverse : bool, optional
        Reverse the hatch mapping.
    """
    if values is None:
        return {}

    if isinstance(hatch_mapping, dict):
        return hatch_mapping

    hatches = resolve_hatches(hatch_mapping, n_hatches=len(values), reverse=reverse)
    return {value: hatch for value, hatch in zip(values, hatches)}