"""
Transparency utilities for publiplots.

This module provides utilities for applying different transparency levels to
face (fill) and edge (outline) of matplotlib artists. This enables the
distinctive publiplots style of transparent fill with opaque edges.
"""

from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba
import numpy as np
from typing import Union, List, Sequence


def apply_transparency(
    artists: Union[PathCollection, Sequence[Patch]],
    face_alpha: float,
    edge_alpha: float = 1.0,
) -> None:
    """
    Apply different alpha transparency to face vs edge of matplotlib artists.

    This function modifies artists in-place to have transparent fill with
    opaque edges, creating the distinctive publiplots visual style. Works
    with both scatter plot collections and bar plot patches.

    The function is safe to call before legend creation, as legends use
    independent custom handles that are not affected by these modifications.

    Parameters
    ----------
    artists : PathCollection or list of Patch
        Matplotlib artists to modify:
        - PathCollection: From scatter plots (ax.collections)
        - List[Patch]: From bar plots (ax.patches)
    face_alpha : float
        Alpha transparency for face/fill color (0.0-1.0).
        0.0 = fully transparent, 1.0 = fully opaque.
    edge_alpha : float, default=1.0
        Alpha transparency for edge/outline color (0.0-1.0).
        Typically kept at 1.0 for opaque edges.

    Returns
    -------
    None
        Modifies artists in-place.

    Examples
    --------
    Apply transparency to scatter plot:
    >>> import publiplots as pp
    >>> import seaborn as sns
    >>> fig, ax = plt.subplots()
    >>> sns.scatterplot(data=df, x='x', y='y', ax=ax)
    >>> pp.apply_edge_transparency(ax.collections[0], face_alpha=0.1)

    Apply transparency to bar plot:
    >>> fig, ax = plt.subplots()
    >>> sns.barplot(data=df, x='category', y='value', ax=ax)
    >>> pp.apply_edge_transparency(ax.patches, face_alpha=0.2)

    Notes
    -----
    - This function is designed to work after seaborn plotting functions
    - Colors are converted to RGBA format with specified alpha values
    - Edge colors default to face colors if not explicitly set
    - Original color values are preserved, only alpha is modified
    """
    if isinstance(artists, PathCollection):
        _apply_to_collection(artists, face_alpha, edge_alpha)
    elif isinstance(artists, Sequence[Line2D]):
        # Assume it's a list/sequence of lines
        _apply_to_lines(artists, face_alpha, edge_alpha)
    elif isinstance(artists, Sequence[Patch]):
        _apply_to_patches(artists, face_alpha, edge_alpha)
    else:
        raise ValueError(f"Unsupported artist type: {type(artists)}")


def _apply_to_collection(
    collection: PathCollection,
    face_alpha: float,
    edge_alpha: float,
) -> None:
    """
    Apply transparency to a PathCollection (scatter plot).

    Parameters
    ----------
    collection : PathCollection
        Scatter plot collection.
    face_alpha : float
        Alpha for face colors.
    edge_alpha : float
        Alpha for edge colors.
    """
    # Get current edge colors as RGBA arrays
    edge_colors = collection.get_edgecolors()

    if len(edge_colors) == 0:
        edge_colors = collection.get_facecolors()

    # Now apply different alpha to face
    new_face_colors = np.array([
        to_rgba(edge_colors[i], alpha=face_alpha)
        for i in range(len(edge_colors))
    ])
    collection.set_facecolors(new_face_colors)

    # Now apply different alpha to edge
    new_edge_colors = np.array([
        to_rgba(edge_colors[i], alpha=edge_alpha)
        for i in range(len(edge_colors))
    ])
    collection.set_edgecolors(new_edge_colors)


def _apply_to_lines(
    lines: Sequence[Line2D],
    face_alpha: float,
    edge_alpha: float,
) -> None:
    """
    Apply transparency to a sequence of Lines (boxplot, swarmplot, etc.).

    Parameters
    ----------
    lines : Sequence[Line2D]
        List of matplotlib lines.
    face_alpha : float
        Alpha for marker face colors.
    edge_alpha : float
        Alpha for marker edge colors.
    """
    for line in lines:
        color = line.get_color()
        if line.get_marker() and line.get_marker() != 'None':
            line.set_markerfacecolor(to_rgba(color, alpha=face_alpha))
            line.set_markeredgecolor(to_rgba(color, alpha=edge_alpha))
        else:
            line.set_color(to_rgba(color, alpha=edge_alpha))

def _apply_to_patches(
    patches: Sequence[Patch],
    face_alpha: float,
    edge_alpha: float,
) -> None:
    """
    Apply transparency to a sequence of Patches (bar plot, etc.).

    Parameters
    ----------
    patches : Sequence[Patch]
        List of matplotlib patches.
    face_alpha : float
        Alpha for face colors.
    edge_alpha : float
        Alpha for edge colors.
    """
    for patch in patches:
        if not hasattr(patch, 'get_edgecolor'):
            # Skip non-patch artists
            continue

        # Get current edge color
        edge_color = patch.get_edgecolor()


        # Now apply different alpha to face and edge
        patch.set_facecolor(to_rgba(edge_color, alpha=face_alpha))
        patch.set_edgecolor(to_rgba(edge_color, alpha=edge_alpha))


__all__ = [
    "apply_transparency",
]
