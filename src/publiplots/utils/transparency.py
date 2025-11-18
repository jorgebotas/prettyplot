"""
Transparency utilities for publiplots.

This module provides utilities for applying different transparency levels to
face (fill) and edge (outline) of matplotlib artists. This enables the
distinctive publiplots style of transparent fill with opaque edges.
"""

from matplotlib.collections import PathCollection
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba
import numpy as np
from typing import Union, List, Sequence


def apply_edge_transparency(
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
    else:
        # Assume it's a list/sequence of patches
        _apply_to_patches(artists, face_alpha, edge_alpha)


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
    # Get current colors as RGBA arrays
    face_colors = collection.get_facecolors()
    edge_colors = collection.get_edgecolors()

    # Handle case where colors might be a single color broadcasted
    # or an array with one color per point
    if len(face_colors) > 0:
        # Apply face alpha to each face color
        new_face_colors = np.array([
            to_rgba(face_colors[i], alpha=face_alpha)
            for i in range(len(face_colors))
        ])
        collection.set_facecolors(new_face_colors)

    if len(edge_colors) > 0:
        # Apply edge alpha to each edge color
        new_edge_colors = np.array([
            to_rgba(edge_colors[i], alpha=edge_alpha)
            for i in range(len(edge_colors))
        ])
        collection.set_edgecolors(new_edge_colors)


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
        if not hasattr(patch, 'get_facecolor'):
            # Skip non-patch artists
            continue

        # Get current colors
        face_color = patch.get_facecolor()
        edge_color = patch.get_edgecolor()

        # Apply new alpha values
        patch.set_facecolor(to_rgba(face_color, alpha=face_alpha))
        patch.set_edgecolor(to_rgba(edge_color, alpha=edge_alpha))


__all__ = [
    "apply_edge_transparency",
]
