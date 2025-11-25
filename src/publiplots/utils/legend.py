"""
Legend handlers for publiplots.

This module provides custom legend handlers for creating publication-ready legends
that match the double-layer plotting style used in publiplots (transparent fill +
solid edge). The handlers automatically create legend markers that match the
visual style of scatterplots and barplots.
"""

from typing import List, Dict, Optional, Tuple, Any, Union

from publiplots.themes.rcparams import resolve_param
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar
from matplotlib.legend import Legend
from matplotlib.legend_handler import HandlerBase, HandlerPatch
from matplotlib.patches import Circle, Rectangle, Patch
import matplotlib.pyplot as plt

# =============================================================================
# Custom Legend Handlers
# =============================================================================

class RectanglePatch(Patch):
    """
    Custom rectangle patch object for legend handles.
    """
    def __init__(self, **kwargs):
        if "markersize" in kwargs:
            del kwargs["markersize"]
        super().__init__(**kwargs)
class MarkerPatch(Patch):
    """
    Custom marker patch object for legend handles.
    Embeds marker symbol and markersize properties.
    """
    def __init__(self, marker='o', **kwargs):
        markersize = kwargs.pop("markersize", plt.rcParams["lines.markersize"])
        self.marker = marker
        self.markersize = markersize
        super().__init__(**kwargs)

    def get_marker(self) -> str:
        return self.marker

    def set_marker(self, marker: str):
        self.marker = marker

    def get_markersize(self) -> float:
        return self.markersize

    def set_markersize(self, markersize: float):
        if markersize is None or markersize == 0:
            markersize = plt.rcParams["lines.markersize"]
        self.markersize = markersize


class HandlerRectangle(HandlerPatch):
    """
    Custom legend handler for double-layer rectangle markers.
    
    Automatically extracts alpha, linewidth, hatches, and colors from handles.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        """Create the legend marker artists."""
        # Rectangle position and size
        x = -xdescent
        y = -ydescent

        # Extract all properties from the handle
        color, alpha, linewidth, edgecolor, hatch_pattern = self._extract_properties(
            orig_handle
        )

        # Create filled rectangle with transparency
        rect_fill = Rectangle(
            (x, y),
            width,
            height,
            facecolor=color,
            edgecolor="none",
            alpha=alpha,
            linewidth=0,
            transform=trans,
            hatch=None,
            zorder=2
        )

        # Create edge rectangle with hatch pattern
        rect_edge = Rectangle(
            (x, y),
            width,
            height,
            alpha=1,
            facecolor="none",
            edgecolor=edgecolor,
            linewidth=linewidth,
            transform=trans,
            hatch=hatch_pattern,
            zorder=3
        )

        return [rect_fill, rect_edge]

    def _extract_properties(
        self,
        orig_handle: Any
    ) -> Tuple[str, float, float, str, Optional[str]]:
        """
        Extract all properties from the handle.
        
        Returns
        -------
        Tuple[str, float, float, str, Optional[str]]
            (color, alpha, linewidth, edgecolor, hatch_pattern)
        """
        # Defaults
        color = "gray"
        alpha = resolve_param("alpha", None)
        linewidth = resolve_param("lines.linewidth", None)
        edgecolor = None
        hatch_pattern = None

        # Extract from Patch
        if hasattr(orig_handle, "get_facecolor"):
            color = orig_handle.get_facecolor()
        if hasattr(orig_handle, "get_edgecolor"):
            edgecolor = orig_handle.get_edgecolor()
        if hasattr(orig_handle, "get_alpha") and orig_handle.get_alpha() is not None:
            alpha = orig_handle.get_alpha()
        if hasattr(orig_handle, "get_linewidth") and orig_handle.get_linewidth():
            linewidth = orig_handle.get_linewidth()
        if hasattr(orig_handle, "get_hatch"):
            hatch_pattern = orig_handle.get_hatch()

        # Handle tuple format (color, hatch, alpha, linewidth)
        if isinstance(orig_handle, tuple):
            if len(orig_handle) >= 1:
                color = orig_handle[0]
            if len(orig_handle) >= 2:
                hatch_pattern = orig_handle[1]
            if len(orig_handle) >= 3:
                alpha = orig_handle[2]
            if len(orig_handle) >= 4:
                linewidth = orig_handle[3]

        # Use face color as edge color if not specified
        if edgecolor is None:
            edgecolor = color

        return color, alpha, linewidth, edgecolor, hatch_pattern


class HandlerMarker(HandlerBase):
    """
    Generic legend handler for any matplotlib marker type.

    Automatically creates double-layer markers (transparent fill + opaque edge)
    for all marker symbols: 'o', '^', 's', 'D', '*', etc.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
    ) -> List:
        """Create the legend marker artists."""
        from matplotlib.lines import Line2D
        from matplotlib.colors import to_rgba

        # Center point for the marker
        cx = 0.5 * width - 0.5 * xdescent
        cy = 0.5 * height - 0.5 * ydescent

        # Extract all properties from the handle
        marker, color, size, alpha, linewidth, edgecolor = self._extract_properties(
            orig_handle, fontsize
        )

        # Create filled marker with transparency
        marker_fill = Line2D(
            [cx], [cy],
            marker=marker,
            markersize=size,
            markerfacecolor=to_rgba(color, alpha),
            markeredgecolor='none',
            linestyle='none',
            transform=trans,
            zorder=2
        )

        # Create edge marker
        marker_edge = Line2D(
            [cx], [cy],
            marker=marker,
            markersize=size,
            markerfacecolor='none',
            markeredgecolor=to_rgba(edgecolor, 1.0),
            markeredgewidth=linewidth,
            linestyle='none',
            transform=trans,
            zorder=3
        )

        return [marker_fill, marker_edge]

    def _extract_properties(
        self,
        orig_handle: Any,
        fontsize: float
    ) -> Tuple[str, str, float, float, float, str]:
        """
        Extract all properties from the handle.

        Returns
        -------
        Tuple[str, str, float, float, float, str]
            (marker, color, size, alpha, linewidth, edgecolor)
        """
        from matplotlib.lines import Line2D

        # Defaults
        marker = 'o'
        color = "gray"
        size = fontsize * 0.8
        alpha = resolve_param("alpha", None)
        linewidth = resolve_param("lines.linewidth", None)
        edgecolor = None

        # Extract from MarkerPatch (created by create_legend_handles)
        if isinstance(orig_handle, MarkerPatch):
            marker = orig_handle.get_marker()
            color = orig_handle.get_facecolor()
            edgecolor = orig_handle.get_edgecolor()
            alpha = orig_handle.get_alpha() if orig_handle.get_alpha() is not None else alpha
            linewidth = orig_handle.get_linewidth() if orig_handle.get_linewidth() else linewidth
            size = orig_handle.get_markersize() if orig_handle.get_markersize() is not None else size

        # Extract from Line2D (standard matplotlib)
        elif isinstance(orig_handle, Line2D):
            marker = orig_handle.get_marker() or 'o'
            color = orig_handle.get_color() or orig_handle.get_markerfacecolor()
            size = orig_handle.get_markersize() or size
            linewidth = orig_handle.get_markeredgewidth() or linewidth
            # Line2D doesn't store alpha separately - use default
            # edgecolor will default to face color below

        # Use face color as edge color if not specified
        if edgecolor is None:
            edgecolor = color

        return marker, color, size, alpha, linewidth, edgecolor


# =============================================================================
# Helper Functions
# =============================================================================


def get_legend_handler_map() -> Dict[type, HandlerBase]:
    """
    Get a handler map for automatic legend styling.

    Returns
    -------
    Dict[type, HandlerBase]
        Dictionary mapping matplotlib types to handler instances.
    """
    handler_rectangle = HandlerRectangle()
    handler_marker = HandlerMarker()

    return {
        Rectangle: handler_rectangle,
        MarkerPatch: handler_marker,
        Patch: handler_rectangle,
    }

def create_legend_handles(
    labels: List[str],
    colors: Optional[List[str]] = None,
    hatches: Optional[List[str]] = None,
    sizes: Optional[List[float]] = None,
    markers: Optional[List[str]] = None,
    alpha: Optional[float] = None,
    linewidth: Optional[float] = None,
    style: str = "rectangle",
    color: Optional[str] = None
) -> List[Patch]:
    """
    Create custom legend handles with alpha and linewidth embedded.

    Parameters
    ----------
    labels : List[str]
        Labels for each legend entry.
    colors : List[str], optional
        Colors for each legend entry.
    hatches : List[str], optional
        Hatch patterns for each legend entry (for rectangles).
    sizes : List[float], optional
        Sizes for each legend entry (markersizes).
    markers : List[str], optional
        Marker symbols for each legend entry (e.g., ['o', '^', 's']).
        If provided, creates MarkerPatch handles regardless of style parameter.
    alpha : float, default=DEFAULT_ALPHA
        Transparency level for fill layers.
    linewidth : float, default=DEFAULT_LINEWIDTH
        Width of edge lines.
    style : str, default="rectangle"
        Style of legend markers: "rectangle", "circle", or "marker".
        Ignored if markers parameter is provided.
    color : str, optional
        Single color for all entries if colors not provided.

    Returns
    -------
    List[Patch]
        List of Patch objects with embedded properties.
    """
    # Read defaults from rcParams if not provided
    alpha = resolve_param("alpha", alpha)
    linewidth = resolve_param("lines.linewidth", linewidth)

    if colors is None:
        default_color = resolve_param("color", None)
        colors = [color if color is not None else default_color] * len(labels)

    if hatches is None or len(hatches) == 0 or style == "circle" or markers is not None:
        hatches = [""] * len(labels)

    if sizes is None or len(sizes) == 0:
        sizes = [plt.rcParams["lines.markersize"]] * len(labels)

    if markers is not None and len(markers) == 0:
        markers = None

    handles = []

    # Determine patch type
    if markers is not None:
        # Use MarkerPatch when markers are specified
        patch = MarkerPatch
        for label, col, hatch, size, marker in zip(labels, colors, hatches, sizes, markers):
            handle = patch(
                marker=marker,
                facecolor=col,
                edgecolor=col,
                alpha=alpha,
                linewidth=linewidth,
                label=label,
                markersize=size
            )
            handles.append(handle)
    else:
        # Use MarkerPatch for circles, RectanglePatch for rectangles
        if style == "circle":
            # Circle is just a marker with 'o' symbol
            for label, col, hatch, size in zip(labels, colors, hatches, sizes):
                handle = MarkerPatch(
                    marker='o',
                    facecolor=col,
                    edgecolor=col,
                    alpha=alpha,
                    linewidth=linewidth,
                    label=label,
                    markersize=size
                )
                handles.append(handle)
        else:
            # Rectangle patches (for bar plots with hatches)
            for label, col, hatch, size in zip(labels, colors, hatches, sizes):
                handle = RectanglePatch(
                    facecolor=col,
                    edgecolor=col,
                    alpha=alpha,
                    linewidth=linewidth,
                    label=label,
                    hatch=hatch,
                    markersize=size
                )
                handles.append(handle)

    return handles


# =============================================================================
# Legend Builder (Primary Interface)
# =============================================================================


class LegendBuilder:
    """
    Modular legend builder for stacking multiple legend types.
    
    This is the primary interface for creating legends in publiplots.
    """
    
    def __init__(
        self,
        ax: Axes,
        bbox_to_anchor: Tuple[float, float] = (1.02, 1),
        spacing: float = 0.03,
    ):
        """
        Parameters
        ----------
        ax : Axes
            Main plot axes.
        x_offset : float
            Horizontal offset from right edge of axes (in axes coordinates).
        spacing : float
            Vertical spacing between elements (in axes coordinates).
        """
        self.ax = ax
        self.fig = ax.get_figure()
        self.x_offset = bbox_to_anchor[0]
        self.current_y = bbox_to_anchor[1]
        self.spacing = spacing
        self.elements = []

    def add_legend(
        self,
        handles: List,
        label: str = "",
        frameon: bool = False,
        **kwargs
    ) -> Legend:
        """
        Add a legend with automatic handler mapping.

        Parameters
        ----------
        handles : list
            Legend handles (from create_legend_handles or plot objects).
        label : str
            Legend label.
        frameon : bool
            Whether to show frame.
        **kwargs
            Additional kwargs for ax.legend().

        Returns
        -------
        Legend
            The created legend object.
        """
        # Pass label to matplotlib's title parameter if provided
        if label:
            kwargs['title'] = label

        default_kwargs = {
            "loc": "upper left",
            "bbox_to_anchor": (self.x_offset, self.current_y),
            "bbox_transform": self.ax.transAxes,
            "frameon": frameon,
            "borderaxespad": 0,
            "borderpad": 0,
            "handletextpad": 0.5,
            "labelspacing": 0.3,
            "handler_map": kwargs.pop("handler_map", get_legend_handler_map()),
            "alignment": "left",
        }
        default_kwargs.update(kwargs)
        
        existing_legends = [e[1] for e in self.elements if e[0] == "legend"]
        leg = self.ax.legend(handles=handles, **default_kwargs)
        leg.set_clip_on(False)
        
        for existing_legend in existing_legends:
            self.ax.add_artist(existing_legend)

        self.elements.append(("legend", leg))
        self._update_position_after_legend(leg)
        
        return leg
    
    def add_colorbar(
        self,
        mappable: ScalarMappable,
        label: str = "",
        height: float = 0.2,
        width: float = 0.05,
        title_position: str = "top",  # "top" or "right"
        title_pad: float = 0.05,
        **kwargs
    ) -> Colorbar:
        """
        Add a colorbar with fixed size and optional title on top.
        
        Parameters
        ----------
        mappable: ScalarMappable
            ScalarMappable object.
        label : str
            Colorbar label.
        height : float
            Height of colorbar (in axes coordinates, e.g., 0.2 = 20% of axes height).
        width : float
            Width of colorbar (in axes coordinates).
        title_position : str
            Position of title: "top" (horizontal, above colorbar) or 
            "right" (vertical, default matplotlib style).
        title_pad : float
            Padding between title and colorbar.
        **kwargs
            Additional kwargs for fig.colorbar().
        
        Returns
        -------
        Colorbar
            The created colorbar object.
        """
        
        # Calculate colorbar position
        ax_pos = self.ax.get_position()

        if title_position == "top" and label:
            # Add title text at current_y
            title_text = self.ax.text(
                self.x_offset, 
                self.current_y,
                label,
                transform=self.ax.transAxes,
                ha="left",
                va="top",  # Align top of text with current_y
                fontsize=plt.rcParams.get("legend.title_fontsize", plt.rcParams["font.size"]),
                fontweight="normal"
            )
            
            # Force draw to measure title height
            self.fig.canvas.draw()
            
            # Get title bounding box in axes coordinates
            bbox = title_text.get_window_extent(self.fig.canvas.get_renderer())
            bbox_axes = bbox.transformed(self.ax.transAxes.inverted())
            title_height = bbox_axes.height

            
            # Update current_y to position colorbar below title
            self.current_y -= title_height + title_pad

        # Convert x_offset from axes coordinates to figure coordinates
        # self.x_offset is in axes coords (e.g., 1.02 = just right of axes)
        cbar_left = ax_pos.x0 + 0.02 + self.x_offset * ax_pos.width
        
        # Position colorbar at current_y (aligned with other legends)
        cbar_bottom = ax_pos.y0 + (self.current_y - height) * ax_pos.height
    
        # Width needs to be in figure coordinates
        cbar_width = width * ax_pos.width
        
        cbar_ax = self.fig.add_axes([
            cbar_left,
            cbar_bottom,
            cbar_width,
            height * ax_pos.height
        ])
        
        default_kwargs = {}
        default_kwargs.update(kwargs)
        
        cbar = self.fig.colorbar(mappable, cax=cbar_ax, **default_kwargs)
        cbar.set_label("" if title_position == "top" else label)
        
        self.elements.append(("colorbar", cbar))
        
        # Update position for next element
        # Add extra spacing for the title if on top
        title_extra_space = 0.04 if title_position == "top" and label else 0
        self.current_y -= (height + self.spacing + title_extra_space)
        
        return cbar
    
    def _update_position_after_legend(self, legend: Legend):
        """Update current_y position after adding a legend."""
        # Force draw to get actual size
        self.fig.canvas.draw()
        
        # Get legend bounding box
        bbox = legend.get_window_extent(self.fig.canvas.get_renderer())
        bbox_axes = bbox.transformed(self.ax.transAxes.inverted())
        height = bbox_axes.height
        
        # Update position for next element
        self.current_y -= (height + self.spacing)
    
    def add_legend_for(self, type: str, label: Optional[str] = None, **kwargs):
        """
        Add legend by auto-detecting from self.ax stored metadata.

        Parameters
        ----------
        type : str
            Type of legend: 'hue', 'size', or 'style'
        label : str, optional
            Legend label (overrides default from metadata).
        **kwargs : dict
            Additional customization passed to add_legend() or add_colorbar()
            (frameon, labelspacing, handletextpad, height, width, etc.)

        Examples
        --------
        >>> builder = pp.legend(ax, auto=False)
        >>> builder.add_legend_for('hue', label='Groups')
        >>> builder.add_legend_for('size', label='Magnitude')
        >>> builder.add_legend_for('hue', label='Score')  # Works for colorbar too
        """
        legend_data = _get_legend_data(self.ax)

        if legend_data and type in legend_data:
            # Use stored metadata
            data = legend_data[type].copy()

            # Check if this is a colorbar
            if data.get('type') == 'colorbar':
                # Handle colorbar
                if label is not None:
                    data['label'] = label
                data.update(kwargs)
                # Remove 'type' key as it's not a parameter for add_colorbar
                data.pop('type', None)
                self.add_colorbar(**data)
            else:
                # Handle regular legend
                if label is not None:
                    data['label'] = label
                data.update(kwargs)
                self.add_legend(**data)
        else:
            # Fallback: basic auto-detection
            # This is a simple fallback - may not work for complex cases
            pass

    def get_remaining_height(self) -> float:
        """Get remaining vertical space."""
        return max(0, self.current_y)


def _get_legend_data(ax: Axes) -> dict:
    """
    Get stored legend data from axes collections/patches/lines.

    Parameters
    ----------
    ax : Axes
        Axes to retrieve legend data from

    Returns
    -------
    dict
        Dictionary with legend data for 'hue', 'size', 'style' if available
    """
    # Check collections first
    for collection in ax.collections:
        if hasattr(collection, '_legend_data'):
            return collection._legend_data

    # Check patches
    for patch in ax.patches:
        if hasattr(patch, '_legend_data'):
            return patch._legend_data

    # Check lines (for pointplot)
    for line in ax.lines:
        if hasattr(line, '_legend_data'):
            return line._legend_data

    return {}


def legend(
    ax: Axes,
    handles: Optional[List] = None,
    labels: Optional[List[str]] = None,
    auto: bool = True,
    **kwargs
) -> LegendBuilder:
    """
    Create publiplots-styled legend. Returns LegendBuilder for further customization.

    This is the primary interface for legend creation in publiplots.

    Parameters
    ----------
    ax : Axes
        Axes to create legend for
    handles : list, optional
        Manual legend handles. If provided, auto is ignored and handles are used directly.
    labels : list, optional
        Manual legend labels (used with handles).
    auto : bool, default=True
        If True, auto-creates all legends from ._legend_data stored on collections.
        If False, returns empty builder for manual control via add_legend_for().
    bbox_to_anchor : tuple, optional
        Bounding box anchor for legend position. Default: (1.02, 1)
    spacing : float, optional
        Vertical spacing between legend elements. Default: 0.03
    **kwargs : dict
        Additional kwargs:
        - If handles provided: passed to add_legend() (frameon, label, etc.)
        - Otherwise: passed to LegendBuilder init (bbox_to_anchor, spacing)

    Returns
    -------
    LegendBuilder
        Builder object for adding more legends or customization.

    Examples
    --------
    Auto mode (creates all legends from stored data):
    >>> fig, ax = pp.scatterplot(data=df, x='x', y='y', hue='group', legend=False)
    >>> builder = pp.legend(ax)  # Auto-creates hue legend

    Manual selective mode:
    >>> builder = pp.legend(ax, auto=False)  # No legends created yet
    >>> builder.add_legend_for('hue', label='Groups')
    >>> builder.add_legend_for('size', label='Magnitude')

    Expert mode with custom handles:
    >>> builder = pp.legend(ax, auto=False)
    >>> builder.add_legend(handles=custom_handles, labels=custom_labels, label='Custom')

    Manual handles mode:
    >>> builder = pp.legend(ax, handles=custom_handles, labels=custom_labels, label='My Legend')
    """
    # Extract LegendBuilder-specific kwargs
    builder_kwargs = {
        'bbox_to_anchor': kwargs.pop('bbox_to_anchor', (1.02, 1)),
        'spacing': kwargs.pop('spacing', 0.03),
    }

    # Initialize LegendBuilder
    builder = LegendBuilder(ax, **builder_kwargs)

    # Auto-apply handler_map if not provided
    if 'handler_map' not in kwargs:
        kwargs['handler_map'] = get_legend_handler_map()

    # Manual mode with handles
    if handles is not None:
        builder.add_legend(handles=handles, labels=labels, **kwargs)
        return builder

    # Auto mode - create all legends from metadata
    if auto:
        legend_data = _get_legend_data(ax)
        if legend_data:
            if 'hue' in legend_data:
                hue_data = legend_data['hue'].copy()
                # Check if it's a colorbar
                if hue_data.get('type') == 'colorbar':
                    hue_data.pop('type', None)
                    builder.add_colorbar(**hue_data)
                else:
                    builder.add_legend(**hue_data, **kwargs)
            if 'size' in legend_data:
                size_data = legend_data['size'].copy()
                builder.add_legend(**size_data, **kwargs)
            if 'style' in legend_data:
                style_data = legend_data['style'].copy()
                builder.add_legend(**style_data, **kwargs)

    # If auto=False, just return empty builder for manual control
    return builder

__all__ = [
    "HandlerRectangle",
    "HandlerMarker",
    "RectanglePatch",
    "MarkerPatch",
    "get_legend_handler_map",
    "create_legend_handles",
    "LegendBuilder",
    "legend",
]