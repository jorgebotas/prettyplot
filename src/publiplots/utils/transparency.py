"""
Transparency utilities for publiplots.

This module provides utilities for applying different transparency levels to
face (fill) and edge (outline) of matplotlib artists. This enables the
distinctive publiplots style of transparent fill with opaque edges.
"""

from matplotlib.collections import PathCollection, FillBetweenPolyCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba
from matplotlib.axes import Axes
import numpy as np
from typing import Union, Sequence, Optional, List


class ArtistTracker:
    """
    Track matplotlib artists added to an axes for selective transparency application.

    This class captures a snapshot of the current artists on an axes, then allows
    applying transparency only to newly added artists. This is useful when overlaying
    multiple plots (e.g., violin + swarm) to avoid modifying previously drawn elements.

    Parameters
    ----------
    ax : Axes
        The matplotlib axes to track.

    Examples
    --------
    >>> tracker = ArtistTracker(ax)
    >>> sns.violinplot(data=df, ax=ax)
    >>> tracker.apply_transparency(face_alpha=0.3)

    >>> # Selective application
    >>> tracker.apply_transparency(on="collections", face_alpha=0.3)
    >>> tracker.apply_transparency(on=["collections", "lines"], face_alpha=0.3)
    """

    def __init__(self, ax: Axes):
        self.ax = ax
        self._snapshot()

    def _snapshot(self) -> None:
        """Capture the current state of artists on the axes."""
        self._collections = set(self.ax.collections)
        self._lines = set(self.ax.lines)
        self._patches = set(self.ax.patches)

    def get_new_collections(self) -> List:
        """Return collections added since snapshot."""
        return [c for c in self.ax.collections if c not in self._collections]

    def get_new_lines(self) -> List:
        """Return lines added since snapshot."""
        return [l for l in self.ax.lines if l not in self._lines]

    def get_new_patches(self) -> List:
        """Return patches added since snapshot."""
        return [p for p in self.ax.patches if p not in self._patches]

    def apply_transparency(
        self,
        on: Optional[Union[str, List[str]]] = None,
        face_alpha: Optional[float] = None,
        edge_alpha: float = 1.0,
    ) -> None:
        """
        Apply transparency to newly added artists.

        Parameters
        ----------
        on : str or list of str, optional
            Which artist types to apply transparency to.
            Options: "collections", "lines", "patches".
            If None, applies to all new artists.
        face_alpha : float, optional
            Alpha transparency for face/fill color (0.0-1.0).
        edge_alpha : float, default=1.0
            Alpha transparency for edge/outline color (0.0-1.0).
        """
        if face_alpha is None:
            return

        # Normalize 'on' parameter to a list
        if on is None:
            targets = ["collections", "lines", "patches"]
        elif isinstance(on, str):
            targets = [on]
        else:
            targets = on

        # Apply to each target type
        if "collections" in targets:
            for collection in self.get_new_collections():
                apply_transparency(collection, face_alpha=face_alpha, edge_alpha=edge_alpha)

        if "lines" in targets:
            new_lines = self.get_new_lines()
            if new_lines:
                apply_transparency(new_lines, face_alpha=face_alpha, edge_alpha=edge_alpha)

        if "patches" in targets:
            new_patches = self.get_new_patches()
            if new_patches:
                apply_transparency(new_patches, face_alpha=face_alpha, edge_alpha=edge_alpha)


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
    if isinstance(artists, PathCollection) or isinstance(artists, FillBetweenPolyCollection):
        _apply_to_collection(artists, face_alpha, edge_alpha)
    elif hasattr(artists, '__iter__') and not isinstance(artists, (str, PathCollection)):
        # It's a sequence - check first element type
        artists_list = list(artists)
        if len(artists_list) == 0:
            return
        if isinstance(artists_list[0], Line2D):
            _apply_to_lines(artists_list, face_alpha, edge_alpha)
        elif isinstance(artists_list[0], Patch):
            _apply_to_patches(artists_list, face_alpha, edge_alpha)
        else:
            raise ValueError(f"Unsupported artist type in sequence: {type(artists_list[0])}")
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
    face_colors = collection.get_facecolors()

    if len(edge_colors) == 0:
        edge_colors = face_colors

    if len(face_colors) == 0:
        face_colors = edge_colors

    # Now apply different alpha to face
    new_face_colors = np.array([
        to_rgba(c, alpha=face_alpha) for c in face_colors
    ])
    collection.set_facecolors(new_face_colors)

    # Now apply different alpha to edge
    new_edge_colors = np.array([
        to_rgba(c, alpha=edge_alpha) for c in edge_colors
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
    "ArtistTracker",
    "apply_transparency",
]
