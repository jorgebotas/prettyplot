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
import matplotlib

# Version checking for matplotlib compatibility
_MPL_VERSION = tuple(int(x) for x in matplotlib.__version__.split('.')[:2])
_HAS_LEGEND_ALIGNMENT = _MPL_VERSION >= (3, 6)


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
class CirclePatch(Patch):
    """
    Custom circle patch object for legend handles.
    Embeds markersize property.
    """
    def __init__(self, **kwargs):
        markersize = kwargs.pop("markersize", plt.rcParams["lines.markersize"])
        self.markersize = markersize
        super().__init__(**kwargs)

    def get_markersize(self) -> float:
        return self.markersize

    def set_markersize(self, markersize: float):
        if markersize is None or markersize == 0:
            markersize = plt.rcParams["lines.markersize"]
        self.markersize = markersize

class HandlerCircle(HandlerBase):
    """
    Custom legend handler for double-layer circle markers.
    
    Automatically extracts alpha, linewidth, and colors from handles.
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
    ) -> List[Circle]:
        """Create the legend marker artists."""
        # Center point for the marker
        cx = 0.5 * width - 0.5 * xdescent
        cy = 0.5 * height - 0.5 * ydescent

        # Extract all properties from the handle
        color, size, alpha, linewidth, edgecolor = self._extract_properties(
            orig_handle, fontsize
        )

        # Create filled circle with transparency
        circle_fill = Circle(
            (cx, cy),
            size / 2,
            color=color,
            alpha=alpha,
            transform=trans,
            linewidth=0,
            zorder=2
        )

        # Create edge circle
        circle_edge = Circle(
            (cx, cy),
            size / 2,
            facecolor="none",
            edgecolor=edgecolor,
            linewidth=linewidth,
            transform=trans,
            alpha=1,
            zorder=3
        )

        return [circle_fill, circle_edge]

    def _extract_properties(
        self,
        orig_handle: Any,
        fontsize: float
    ) -> Tuple[str, float, float, float, str]:
        """
        Extract all properties from the handle.
        
        Returns
        -------
        Tuple[str, float, float, float, str]
            (color, size, alpha, linewidth, edgecolor)
        """
        # Defaults
        color = "gray"
        size = fontsize * 0.8
        alpha = resolve_param("alpha", None)
        linewidth = resolve_param("lines.linewidth", None)
        edgecolor = None

        # Extract from Patch (created by create_legend_handles)
        if isinstance(orig_handle, CirclePatch):
            color = orig_handle.get_facecolor()
            edgecolor = orig_handle.get_edgecolor()
            alpha = orig_handle.get_alpha() if orig_handle.get_alpha() is not None else alpha
            linewidth = orig_handle.get_linewidth() if orig_handle.get_linewidth() else linewidth
            size = orig_handle.get_markersize() if orig_handle.get_markersize() is not None else size
        
        # Use face color as edge color if not specified
        if edgecolor is None:
            edgecolor = color

        return color, size, alpha, linewidth, edgecolor

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
    handler_circle = HandlerCircle()
    handler_rectangle = HandlerRectangle()
    
    return {
        Rectangle: handler_rectangle,
        CirclePatch: handler_circle,
        Patch: handler_rectangle,
    }

def create_legend_handles(
    labels: List[str],
    colors: Optional[List[str]] = None,
    hatches: Optional[List[str]] = None,
    sizes: Optional[List[float]] = None,
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
        Hatch patterns for each legend entry.
    sizes : List[float], optional
        Sizes for each legend entry.
    alpha : float, default=DEFAULT_ALPHA
        Transparency level for fill layers.
    linewidth : float, default=DEFAULT_LINEWIDTH
        Width of edge lines.
    style : str, default="rectangle"
        Style of legend markers: "rectangle" or "circle".
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

    if hatches is None or len(hatches) == 0 or style == "circle":
        hatches = [""] * len(labels)

    if sizes is None or len(sizes) == 0:
        sizes = [plt.rcParams["lines.markersize"]] * len(labels)

    handles = []
    patch = CirclePatch if style == "circle" else RectanglePatch
    for label, col, hatch, size in zip(labels, colors, hatches, sizes):
        handle = patch(
            facecolor=col,
            edgecolor=col,
            alpha=alpha,  # Store alpha in handle
            linewidth=linewidth,  # Store linewidth in handle
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
        title: str = "",
        frameon: bool = False,
        **kwargs
    ) -> Legend:
        """
        Add a legend with automatic handler mapping.
        
        Parameters
        ----------
        handles : list
            Legend handles (from create_legend_handles or plot objects).
        title : str
            Legend title.
        frameon : bool
            Whether to show frame.
        **kwargs
            Additional kwargs for ax.legend().
        
        Returns
        -------
        Legend
            The created legend object.
        """
        default_kwargs = {
            "loc": "upper left",
            "bbox_to_anchor": (self.x_offset, self.current_y),
            "bbox_transform": self.ax.transAxes,
            "title": title,
            "frameon": frameon,
            "borderaxespad": 0,
            "borderpad": 0,
            "handletextpad": 0.5,
            "labelspacing": 0.3,
            "handler_map": kwargs.pop("handler_map", get_legend_handler_map())
        }
        # Add alignment parameter only for matplotlib >= 3.6
        if _HAS_LEGEND_ALIGNMENT:
            default_kwargs["alignment"] = "left"
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
    
    def get_remaining_height(self) -> float:
        """Get remaining vertical space."""
        return max(0, self.current_y)


def create_legend_builder(
        ax: Axes,
        bbox_to_anchor: Tuple[float, float] = (1.02, 1),
        spacing: float = 0.03,
    ) -> LegendBuilder:
    """
    Create a LegendBuilder for modular legend construction.
    
    This is the primary way to create legends in publiplots.
    
    Parameters
    ----------
    ax : Axes
        Main plot axes.
    bbox_to_anchor : Tuple[float, float]
        Bounding box to anchor the legend to.
    spacing : float
        Vertical spacing between elements.
    
    Returns
    -------
    LegendBuilder
        Builder object for adding legends.
    
    Examples
    --------
    >>> fig, ax = pp.scatterplot(data=df, x="x", y="y", hue="temp", legend=False)
    >>> builder = pp.create_legend_builder(ax)
    >>> builder.add_colorbar(label="Temperature", title_position="top")
    >>> builder.add_legend(size_handles, title="Size")
    """
    return LegendBuilder(ax, bbox_to_anchor=bbox_to_anchor, spacing=spacing)

__all__ = [
    "HandlerCircle",
    "HandlerRectangle",
    "get_legend_handler_map",
    "create_legend_handles",
    "LegendBuilder",
    "create_legend_builder",
]