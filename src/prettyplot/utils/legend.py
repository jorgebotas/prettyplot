"""
Legend handlers for prettyplot.

This module provides custom legend handlers for creating publication-ready legends
that match the double-layer plotting style used in prettyplot (transparent fill +
solid edge). The handlers automatically create legend markers that match the
visual style of scatterplots and barplots.

The module provides:
    - HandlerCircle: For scatterplot markers (double-layer circles)
    - HandlerRectangle: For barplot markers (double-layer rectangles with hatch support)
    - Helper functions for automatic handler application
"""

from typing import List, Dict, Optional, Tuple, Any, Union
from matplotlib.legend_handler import HandlerBase, HandlerPatch
from matplotlib.patches import Circle, Rectangle, Patch
from matplotlib.collections import PathCollection
from matplotlib.axes import Axes
from matplotlib.legend import Legend

from prettyplot.config import DEFAULT_ALPHA, DEFAULT_LINEWIDTH, DEFAULT_MARKER_SIZE, DEFAULT_COLOR


# =============================================================================
# Custom Legend Handlers
# =============================================================================


class HandlerCircle(HandlerBase):
    """
    Custom legend handler for double-layer circle markers.

    Creates markers with transparent fill and solid borders for use in legends,
    maintaining consistency with prettyplot's scatterplot style. This handler
    produces the same visual appearance as the double-layer markers used in
    scatterplots (fill layer + edge layer).

    Parameters
    ----------
    alpha : float, default=DEFAULT_ALPHA (0.1)
        Transparency level for the fill layer (0-1).
    linewidth : float, default=DEFAULT_LINEWIDTH (2.0)
        Width of the edge circle.
    markersize : float, optional
        Size of the marker in points. If None, uses size from handle or
        DEFAULT_MARKER_SIZE.
    edgecolor : str, optional
        Color for the edge. If None, uses same color as fill.
    **kwargs
        Additional keyword arguments passed to HandlerBase.

    Examples
    --------
    Use with ax.legend():
    >>> from matplotlib.collections import PathCollection
    >>> handler_map = {PathCollection: HandlerCircle()}
    >>> ax.legend(handler_map=handler_map)

    Customize handler parameters:
    >>> handler = HandlerCircle(alpha=0.2, linewidth=3, markersize=12)
    >>> ax.legend(handler_map={PathCollection: handler})

    See Also
    --------
    HandlerRectangle : Handler for barplot rectangles
    legend : Convenience function that applies handlers automatically
    """

    def __init__(
        self,
        alpha: float = DEFAULT_ALPHA,
        linewidth: float = DEFAULT_LINEWIDTH,
        markersize: Optional[float] = None,
        edgecolor: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.linewidth = linewidth
        self.markersize = markersize
        self.edgecolor = edgecolor

    def create_artists(
        self,
        legend: Legend,
        orig_handle: Any,
        xdescent: float,
        ydescent: float,
        width: float,
        height: float,
        fontsize: float,
        trans: Any
    ) -> List[Circle]:
        """
        Create the legend marker artists.

        This method is called by matplotlib to create the visual representation
        of the marker in the legend. It creates two circles: one for the fill
        and one for the edge.

        Parameters
        ----------
        legend : Legend
            The legend instance.
        orig_handle : Any
            The original plot element (e.g., PathCollection, tuple).
        xdescent, ydescent : float
            Descent values for positioning.
        width, height : float
            Width and height of the legend marker box.
        fontsize : float
            Font size for the legend.
        trans : Transform
            Matplotlib transform for the legend marker.

        Returns
        -------
        List[Circle]
            List containing the fill and edge circle artists.
        """
        # Center point for the marker
        cx = 0.5 * width - 0.5 * xdescent
        cy = 0.5 * height - 0.5 * ydescent

        # Extract properties from the handle
        color, size = self._extract_properties(orig_handle, fontsize)

        # Use custom edgecolor if provided
        edge_color = self.edgecolor if self.edgecolor is not None else color

        # Create filled circle with transparency
        circle_fill = Circle(
            (cx, cy),
            size / 2,
            color=color,
            alpha=self.alpha,
            transform=trans,
            linewidth=0,
            zorder=2
        )

        # Create edge circle
        circle_edge = Circle(
            (cx, cy),
            size / 2,
            facecolor="none",
            edgecolor=edge_color,
            linewidth=self.linewidth,
            transform=trans,
            zorder=3
        )

        return [circle_fill, circle_edge]

    def _extract_properties(
        self,
        orig_handle: Any,
        fontsize: float
    ) -> Tuple[str, float]:
        """
        Extract color and size properties from the original handle.

        Parameters
        ----------
        orig_handle : Any
            The original plot element.
        fontsize : float
            Font size for fallback size calculation.

        Returns
        -------
        Tuple[str, float]
            (color, size) extracted from the handle.
        """
        # Handle tuple format (color, size)
        if isinstance(orig_handle, tuple):
            if len(orig_handle) >= 2:
                return orig_handle[0], orig_handle[1]
            elif len(orig_handle) == 1:
                return orig_handle[0], self._get_default_size(fontsize)

        # Extract from PathCollection (scatterplot)
        if isinstance(orig_handle, PathCollection):
            # Get color from face colors
            facecolors = orig_handle.get_facecolors()
            if len(facecolors) > 0:
                color = facecolors[0]
            else:
                color = "gray"

            # Get size from sizes array
            sizes = orig_handle.get_sizes()
            if len(sizes) > 0:
                # Convert from area to diameter for Circle
                size = (sizes[0] ** 0.5) / 2
            else:
                size = self._get_default_size(fontsize)

            return color, size

        # Extract from generic patch-like objects
        if hasattr(orig_handle, "get_facecolor"):
            color = orig_handle.get_facecolor()
        elif hasattr(orig_handle, "get_color"):
            color = orig_handle.get_color()
        else:
            color = "gray"

        # Try to get marker size
        if hasattr(orig_handle, "get_markersize"):
            size = orig_handle.get_markersize()
        else:
            size = self._get_default_size(fontsize)

        return color, size

    def _get_default_size(self, fontsize: float) -> float:
        """Get default marker size based on fontsize or config."""
        if self.markersize is not None:
            return self.markersize
        # Use fontsize as base for marker size
        return fontsize * 0.8


class HandlerRectangle(HandlerPatch):
    """
    Custom legend handler for double-layer rectangle markers.

    Creates rectangles with transparent fill and solid borders for use in legends,
    maintaining consistency with prettyplot's barplot style. Supports hatch
    patterns on the edge layer, matching the hatching used in barplots.

    Parameters
    ----------
    alpha : float, default=DEFAULT_ALPHA (0.1)
        Transparency level for the fill layer (0-1).
    linewidth : float, default=DEFAULT_LINEWIDTH (2.0)
        Width of the edge rectangle.
    hatch : str, optional
        Hatch pattern to apply to the edge layer (e.g., '///', '|||', 'xxx').
        If None, attempts to extract from the handle.
    edgecolor : str, optional
        Color for the edge. If None, uses same color as fill.
    **kwargs
        Additional keyword arguments passed to HandlerPatch.

    Examples
    --------
    Use with ax.legend():
    >>> from matplotlib.patches import Rectangle
    >>> handler_map = {Rectangle: HandlerRectangle()}
    >>> ax.legend(handler_map=handler_map)

    Customize with hatch pattern:
    >>> handler = HandlerRectangle(alpha=0.15, linewidth=2.5, hatch='///')
    >>> ax.legend(handler_map={Rectangle: handler})

    Use with custom handles:
    >>> from matplotlib.patches import Patch
    >>> handles = [
    ...     Patch(facecolor='red', edgecolor='red', hatch='', label='Control'),
    ...     Patch(facecolor='blue', edgecolor='blue', hatch='///', label='Treatment')
    ... ]
    >>> ax.legend(handles=handles, handler_map={Patch: HandlerRectangle()})

    See Also
    --------
    HandlerCircle : Handler for scatterplot circles
    legend : Convenience function that applies handlers automatically
    """

    def __init__(
        self,
        alpha: float = DEFAULT_ALPHA,
        linewidth: float = DEFAULT_LINEWIDTH,
        hatch: Optional[str] = None,
        edgecolor: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.linewidth = linewidth
        self.hatch = hatch
        self.edgecolor = edgecolor

    def create_artists(
        self,
        legend: Legend,
        orig_handle: Any,
        xdescent: float,
        ydescent: float,
        width: float,
        height: float,
        fontsize: float,
        trans: Any
    ) -> List[Rectangle]:
        """
        Create the legend marker artists.

        This method is called by matplotlib to create the visual representation
        of the rectangle marker in the legend. It creates two rectangles: one for
        the fill and one for the edge (with optional hatch pattern).

        Parameters
        ----------
        legend : Legend
            The legend instance.
        orig_handle : Any
            The original plot element (e.g., Rectangle, Patch, tuple).
        xdescent, ydescent : float
            Descent values for positioning.
        width, height : float
            Width and height of the legend marker box.
        fontsize : float
            Font size for the legend.
        trans : Transform
            Matplotlib transform for the legend marker.

        Returns
        -------
        List[Rectangle]
            List containing the fill and edge rectangle artists.
        """
        # Rectangle position and size
        x = -xdescent
        y = -ydescent

        # Extract properties from the handle
        color, hatch_pattern = self._extract_properties(orig_handle)

        # Use custom edgecolor if provided
        edge_color = self.edgecolor if self.edgecolor is not None else color

        # Create filled rectangle with transparency
        rect_fill = Rectangle(
            (x, y),
            width,
            height,
            facecolor=color,
            edgecolor="none",
            alpha=self.alpha,
            linewidth=0,
            transform=trans,
            hatch=None,  # No hatch on fill layer
            zorder=2
        )

        # Create edge rectangle with hatch pattern
        rect_edge = Rectangle(
            (x, y),
            width,
            height,
            facecolor="none",
            edgecolor=edge_color,
            linewidth=self.linewidth,
            transform=trans,
            hatch=hatch_pattern,  # Hatch only on edge layer
            hatch_linewidth=self.linewidth,
            zorder=3
        )

        return [rect_fill, rect_edge]

    def _extract_properties(self, orig_handle: Any) -> Tuple[str, Optional[str]]:
        """
        Extract color and hatch pattern from the original handle.

        Parameters
        ----------
        orig_handle : Any
            The original plot element.

        Returns
        -------
        Tuple[str, Optional[str]]
            (color, hatch_pattern) extracted from the handle.
        """
        # Handle tuple format (color, hatch) or (color,)
        if isinstance(orig_handle, tuple):
            if len(orig_handle) >= 2:
                return orig_handle[0], orig_handle[1]
            elif len(orig_handle) == 1:
                return orig_handle[0], self.hatch

        # Extract color
        if hasattr(orig_handle, "get_facecolor"):
            color = orig_handle.get_facecolor()
        elif hasattr(orig_handle, "get_color"):
            color = orig_handle.get_color()
        else:
            color = "gray"

        # Extract hatch pattern
        hatch_pattern = self.hatch
        if hatch_pattern is None and hasattr(orig_handle, "get_hatch"):
            hatch_pattern = orig_handle.get_hatch()

        return color, hatch_pattern


# =============================================================================
# Helper Functions for Automatic Handler Application
# =============================================================================


def get_legend_handler_map(
    alpha: float = DEFAULT_ALPHA,
    linewidth: float = DEFAULT_LINEWIDTH,
    circle_markersize: Optional[float] = None,
    edgecolor: Optional[str] = None,
) -> Dict[type, HandlerBase]:
    """
    Get a handler map for automatic legend styling.

    Returns a dictionary mapping matplotlib object types to custom handlers
    that create double-layer legend markers matching prettyplot's visual style.
    This map can be passed to ax.legend() or fig.legend() via the handler_map
    parameter.

    Parameters
    ----------
    alpha : float, default=DEFAULT_ALPHA (0.1)
        Transparency level for fill layers in legend markers.
    linewidth : float, default=DEFAULT_LINEWIDTH (2.0)
        Width of edge lines in legend markers.
    circle_markersize : float, optional
        Size of circle markers in legend. If None, uses default based on fontsize.
    edgecolor : str, optional
        Color for edges. If None, uses same color as fill.

    Returns
    -------
    Dict[type, HandlerBase]
        Dictionary mapping matplotlib types to handler instances.

    Examples
    --------
    Use with ax.legend():
    >>> handler_map = pp.get_legend_handler_map()
    >>> ax.legend(handler_map=handler_map)

    Customize handler parameters:
    >>> handler_map = pp.get_legend_handler_map(alpha=0.2, linewidth=3)
    >>> ax.legend(handler_map=handler_map)

    See Also
    --------
    legend : Convenience function that applies handlers automatically
    HandlerCircle : Handler for scatterplot markers
    HandlerRectangle : Handler for barplot markers
    """
    return {
        PathCollection: HandlerCircle(
            alpha=alpha,
            linewidth=linewidth,
            markersize=circle_markersize,
            edgecolor=edgecolor
        ),
        Rectangle: HandlerRectangle(
            alpha=alpha,
            linewidth=linewidth,
            edgecolor=edgecolor
        ),
        Patch: HandlerRectangle(
            alpha=alpha,
            linewidth=linewidth,
            edgecolor=edgecolor
        ),
    }


def legend(
    ax: Optional[Axes] = None,
    alpha: float = DEFAULT_ALPHA,
    linewidth: float = DEFAULT_LINEWIDTH,
    circle_markersize: Optional[float] = None,
    edgecolor: Optional[str] = None,
    handler_map: Optional[Dict[type, HandlerBase]] = None,
    **kwargs
) -> Legend:
    """
    Create a legend with prettyplot's custom handlers.

    This is a convenience function that wraps matplotlib's ax.legend() but
    automatically applies prettyplot's custom legend handlers for double-layer
    markers. It ensures legend markers match the visual style of the plot
    (transparent fill + solid edge).

    Parameters
    ----------
    ax : Axes, optional
        Matplotlib axes object. If None, uses current axes (plt.gca()).
    alpha : float, default=DEFAULT_ALPHA (0.1)
        Transparency level for fill layers in legend markers.
    linewidth : float, default=DEFAULT_LINEWIDTH (2.0)
        Width of edge lines in legend markers.
    circle_markersize : float, optional
        Size of circle markers in legend. If None, uses default based on fontsize.
    edgecolor : str, optional
        Color for edges. If None, uses same color as fill.
    handler_map : dict, optional
        Custom handler map. If provided, merged with default handlers.
    **kwargs
        Additional keyword arguments passed to ax.legend().

    Returns
    -------
    Legend
        Matplotlib Legend instance.

    Examples
    --------
    Basic usage with scatterplot:
    >>> fig, ax = pp.scatterplot(data=df, x='x', y='y', hue='group')
    >>> pp.legend(ax)

    Customize legend position:
    >>> pp.legend(ax, loc='upper right', frameon=False)

    Customize handler parameters:
    >>> pp.legend(ax, alpha=0.2, linewidth=3)

    Add custom handles:
    >>> from matplotlib.patches import Patch
    >>> handles = [Patch(color='red', label='Group A')]
    >>> pp.legend(ax, handles=handles)

    Notes
    -----
    This function automatically detects the plot type (scatterplot, barplot, etc.)
    and applies the appropriate handler. For mixed plots, you may need to provide
    custom handles to ensure proper legend display.

    See Also
    --------
    get_legend_handler_map : Get handler map for manual use
    HandlerCircle : Handler for scatterplot markers
    HandlerRectangle : Handler for barplot markers
    """
    # Get current axes if not provided
    if ax is None:
        import matplotlib.pyplot as plt
        ax = plt.gca()

    # Get default handler map
    default_handler_map = get_legend_handler_map(
        alpha=alpha,
        linewidth=linewidth,
        circle_markersize=circle_markersize,
        edgecolor=edgecolor
    )

    # Merge with user-provided handler map
    if handler_map is not None:
        default_handler_map.update(handler_map)

    # Create legend with custom handlers
    return ax.legend(handler_map=default_handler_map, **kwargs)


# =============================================================================
# Utility Functions
# =============================================================================


def create_legend_handles(
    labels: List[str],
    colors: Optional[List[str]],
    hatches: Optional[List[str]] = None,
    style: str = 'rectangle'
) -> List[Patch]:
    """
    Create custom legend handles for manual legend creation.

    This utility function creates Patch objects that can be used with
    ax.legend(handles=...) to create custom legends. Useful when you need
    manual control over legend content or when combining multiple plot types.

    Parameters
    ----------
    labels : List[str]
        Labels for each legend entry.
    colors : List[str]
        Colors for each legend entry.
    hatches : List[str], optional
        Hatch patterns for each legend entry. If None, no hatches are used.
        Only applicable for 'rectangle' style.
    style : str, default='rectangle'
        Style of legend markers: 'rectangle' or 'circle'.

    Returns
    -------
    List[Patch]
        List of Patch objects suitable for use with ax.legend().

    Examples
    --------
    Create manual legend for barplot:
    >>> handles = pp.create_legend_handles(
    ...     labels=['Control', 'Treatment'],
    ...     colors=['#75b375', '#8e8ec1'],
    ...     hatches=['', '///']
    ... )
    >>> pp.legend(ax, handles=handles)

    Create legend for scatterplot (circles):
    >>> handles = pp.create_legend_handles(
    ...     labels=['Group A', 'Group B'],
    ...     colors=['red', 'blue'],
    ...     style='circle'
    ... )
    >>> pp.legend(ax, handles=handles)

    See Also
    --------
    legend : Create legend with automatic handlers
    """
    handles = []

    if colors is None:
        colors = [DEFAULT_COLOR] * len(labels)

    # Ensure hatches list matches length of labels if provided
    if hatches is None or len(hatches) == 0:
        hatches = [''] * len(labels)
    elif len(hatches) != len(labels):
        # Cycle hatches to match labels length
        hatches = [hatches[i % len(hatches)] for i in range(len(labels))]

    # Create handles based on style
    for label, color, hatch in zip(labels, colors, hatches):
        handle = Patch(
            facecolor=color,
            edgecolor=color,
            label=label,
            hatch=hatch if style == 'rectangle' else None,
        )
        handles.append(handle)

    return handles


__all__ = [
    'HandlerCircle',
    'HandlerRectangle',
    'get_legend_handler_map',
    'legend',
    'create_legend_handles',
]
