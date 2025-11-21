"""
Set logic and label generation for Venn diagrams.

This module handles the logical operations on sets to determine intersection sizes
and generate appropriate labels for each region (petal) of the Venn diagram.
"""

from typing import List, Dict, Iterator


def generate_logics(n_sets: int) -> Iterator[str]:
    """
    Generate binary intersection identifiers for all possible set combinations.

    This function produces binary strings representing which sets participate in
    each intersection. For n sets, it generates 2^n - 1 different combinations
    (excluding the empty set). Each character in the string represents whether
    that set is included ('1') or excluded ('0').

    Parameters
    ----------
    n_sets : int
        Number of sets in the Venn diagram (2-6)

    Yields
    ------
    str
        Binary string of length n_sets, e.g., for 3 sets: '001', '010', '011', etc.
        The rightmost bit corresponds to the first set, leftmost to the last set.

    Examples
    --------
    >>> list(generate_logics(2))
    ['01', '10', '11']

    >>> list(generate_logics(3))
    ['001', '010', '011', '100', '101', '110', '111']

    Notes
    -----
    The binary logic strings are generated in ascending order of their decimal value.
    For example, with 3 sets:
    - '001': only set 0 (first set)
    - '010': only set 1 (second set)
    - '011': sets 0 and 1
    - '100': only set 2 (third set)
    - '101': sets 0 and 2
    - '110': sets 1 and 2
    - '111': all three sets
    """
    for i in range(1, 2**n_sets):
        yield bin(i)[2:].zfill(n_sets)


def generate_petal_labels(
    datasets: List[set],
    fmt: str = "{size}"
) -> Dict[str, str]:
    """
    Generate labels for each region (petal) of the Venn diagram based on set intersections.

    This function calculates the size of each possible intersection in the Venn diagram
    and formats them according to the provided format string. Each region is identified
    by a binary logic string indicating which sets participate in that intersection.

    Parameters
    ----------
    datasets : list of set
        List of sets to analyze. Should contain 2-6 sets.
    fmt : str, default='{size}'
        Format string for labels. Can include:
        - {size}: number of elements in the intersection
        - {logic}: binary string representing the intersection (e.g., '101')
        - {percentage}: percentage of total elements in this intersection

    Returns
    -------
    dict
        Dictionary mapping binary logic strings to formatted label strings.
        Keys are logic strings (e.g., '01', '10', '11' for 2 sets).
        Values are formatted labels for display in the diagram.

    Examples
    --------
    >>> set1 = {1, 2, 3, 4}
    >>> set2 = {3, 4, 5, 6}
    >>> labels = generate_petal_labels([set1, set2])
    >>> labels
    {'01': '2', '10': '2', '11': '2'}

    >>> # With percentage format
    >>> labels = generate_petal_labels([set1, set2], fmt="{size} ({percentage:.1f}%)")
    >>> labels
    {'01': '2 (33.3%)', '10': '2 (33.3%)', '11': '2 (33.3%)'}

    >>> # For 3 sets
    >>> set3 = {4, 5, 6, 7}
    >>> labels = generate_petal_labels([set1, set2, set3])
    >>> # Returns labels for all 7 possible intersections

    Notes
    -----
    The function computes each intersection by:
    1. Taking the union of all included sets (where logic bit is '1')
    2. Subtracting all excluded sets (where logic bit is '0')
    3. Counting the resulting elements

    For example, logic '101' for 3 sets means:
    - Include set 0 and set 2
    - Exclude set 1
    - Result: (set0 ∩ set2) - set1
    """
    datasets = list(datasets)
    n_sets = len(datasets)
    dataset_union = set.union(*datasets)
    universe_size = len(dataset_union)
    petal_labels = {}

    for logic in generate_logics(n_sets):
        # Determine which sets to include and exclude based on binary logic
        included_sets = [
            datasets[i] for i in range(n_sets) if logic[i] == "1"
        ]
        excluded_sets = [
            datasets[i] for i in range(n_sets) if logic[i] == "0"
        ]

        # Calculate the intersection: (intersection of included) - (union of excluded)
        petal_set = (
            (dataset_union & set.intersection(*included_sets)) -
            set.union(set(), *excluded_sets)
        )

        # Format the label
        petal_labels[logic] = fmt.format(
            logic=logic,
            size=len(petal_set),
            percentage=(100 * len(petal_set) / max(universe_size, 1))
        )

    return petal_labels


def get_n_sets(petal_labels: Dict[str, str], dataset_labels: List[str]) -> int:
    """
    Infer and validate the number of sets from petal and dataset labels.

    This function determines the number of sets in the Venn diagram and checks
    that the petal labels are consistent with the dataset labels. It validates
    that all logic strings have the correct length and contain only binary digits.

    Parameters
    ----------
    petal_labels : dict
        Dictionary mapping binary logic strings to label values
    dataset_labels : list of str
        List of dataset names/labels

    Returns
    -------
    int
        Number of sets in the Venn diagram

    Raises
    ------
    ValueError
        If the length of logic strings doesn't match the number of datasets
    KeyError
        If a logic string contains non-binary characters

    Examples
    --------
    >>> petal_labels = {'01': '5', '10': '3', '11': '2'}
    >>> dataset_labels = ['Set A', 'Set B']
    >>> get_n_sets(petal_labels, dataset_labels)
    2

    >>> # Inconsistent lengths will raise an error
    >>> petal_labels = {'001': '5', '010': '3'}
    >>> dataset_labels = ['Set A', 'Set B']  # Only 2 labels but 3-set logic
    >>> get_n_sets(petal_labels, dataset_labels)
    ValueError: Inconsistent petal and dataset labels
    """
    n_sets = len(dataset_labels)
    for logic in petal_labels.keys():
        if len(logic) != n_sets:
            raise ValueError("Inconsistent petal and dataset labels")
        if not (set(logic) <= {"0", "1"}):
            raise KeyError("Key not understood: " + logic)
    return n_sets
