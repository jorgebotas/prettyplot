"""
Core drawing functions for Venn diagrams.

This module provides the fundamental drawing primitives for creating Venn diagrams,
including functions to draw ellipses, triangles, and text labels on matplotlib axes.

Adapted from pyvenn by LankyCyril (https://github.com/LankyCyril/pyvenn)
"""

from matplotlib.pyplot import subplots
from matplotlib.patches import Ellipse, Polygon
from matplotlib.colors import to_rgba
from matplotlib.axes import Axes
from typing import Tuple, Optional


def less_transparent_color(color, alpha_factor: float = 2) -> Tuple[float, float, float, float]:
    """
    Increase the opacity (alpha value) of a color.

    This function takes a color and increases its alpha (opacity) value to make it
    less transparent. This is useful for edge colors that should be more visible
    than fill colors.

    Parameters
    ----------
    color : color-like
        Any matplotlib-compatible color specification (string name, hex code, RGB tuple, etc.)
    alpha_factor : float, default=2
        Factor by which to reduce transparency. Higher values create more opaque colors.
        The new alpha is calculated as: (1 + current_alpha) / alpha_factor

    Returns
    -------
    tuple
        RGBA tuple (red, green, blue, alpha) with increased opacity

    Examples
    --------
    >>> less_transparent_color('red', alpha_factor=2)
    (1.0, 0.0, 0.0, 0.5)

    >>> less_transparent_color((1.0, 0.0, 0.0, 0.3), alpha_factor=2)
    (1.0, 0.0, 0.0, 0.65)
    """
    new_alpha = (1 + to_rgba(color)[3]) / alpha_factor
    return to_rgba(color, alpha=new_alpha)


def draw_ellipse(ax: Axes, x: float, y: float, w: float, h: float, a: float, color) -> None:
    """
    Draw an ellipse on the given matplotlib axes.

    This function creates an ellipse patch with specified position, dimensions,
    rotation angle, and color. The ellipse is filled with the given color and
    outlined with a less transparent version of the same color.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to draw the ellipse
    x : float
        X-coordinate of the ellipse center (normalized coordinates 0-1)
    y : float
        Y-coordinate of the ellipse center (normalized coordinates 0-1)
    w : float
        Width of the ellipse (normalized coordinates)
    h : float
        Height of the ellipse (normalized coordinates)
    a : float
        Rotation angle of the ellipse in degrees (counterclockwise from horizontal)
    color : color-like
        Fill color for the ellipse (any matplotlib-compatible color specification)

    Returns
    -------
    None
        Modifies the axes in-place by adding the ellipse patch

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> draw_ellipse(ax, 0.5, 0.5, 0.3, 0.2, 45, 'blue')
    """
    ax.add_patch(
        Ellipse(
            xy=(x, y),
            width=w,
            height=h,
            angle=a,
            facecolor=color,
            edgecolor=less_transparent_color(color)
        )
    )


def draw_triangle(ax: Axes, x1: float, y1: float, x2: float, y2: float,
                  x3: float, y3: float, _dim, _angle, color) -> None:
    """
    Draw a triangle on the given matplotlib axes.

    This function creates a triangular polygon patch defined by three vertices.
    The triangle is filled with the given color and outlined with a less transparent
    version of the same color. This is used for 6-set Venn diagrams where triangles
    are more suitable than ellipses.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to draw the triangle
    x1, y1 : float
        Coordinates of the first vertex (normalized coordinates 0-1)
    x2, y2 : float
        Coordinates of the second vertex (normalized coordinates 0-1)
    x3, y3 : float
        Coordinates of the third vertex (normalized coordinates 0-1)
    _dim : None
        Unused parameter for API compatibility with draw_ellipse
    _angle : None
        Unused parameter for API compatibility with draw_ellipse
    color : color-like
        Fill color for the triangle (any matplotlib-compatible color specification)

    Returns
    -------
    None
        Modifies the axes in-place by adding the triangle patch

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> draw_triangle(ax, 0.5, 0.8, 0.3, 0.2, 0.7, 0.2, None, None, 'red')
    """
    ax.add_patch(
        Polygon(
            xy=[(x1, y1), (x2, y2), (x3, y3)],
            closed=True,
            facecolor=color,
            edgecolor=less_transparent_color(color)
        )
    )


def draw_text(ax: Axes, x: float, y: float, text: str, fontsize: int,
              color: str = "black") -> None:
    """
    Draw centered text at a specified position on the axes.

    This function places text at the given coordinates with center alignment
    both horizontally and vertically. It's used for labeling regions in the
    Venn diagram with intersection sizes or other information.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to draw the text
    x : float
        X-coordinate for text center (normalized coordinates 0-1)
    y : float
        Y-coordinate for text center (normalized coordinates 0-1)
    text : str
        The text string to display
    fontsize : int
        Font size in points
    color : str, default='black'
        Text color (any matplotlib-compatible color specification)

    Returns
    -------
    None
        Modifies the axes in-place by adding the text

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> draw_text(ax, 0.5, 0.5, '42', fontsize=12, color='black')
    """
    ax.text(
        x, y, text,
        fontsize=fontsize,
        color=color,
        horizontalalignment="center",
        verticalalignment="center"
    )


def init_axes(ax: Optional[Axes], figsize: Tuple[float, float]) -> Axes:
    """
    Initialize or configure axes for Venn diagram plotting.

    This function creates new axes if none are provided, or configures existing axes
    with the appropriate settings for Venn diagrams. It sets up an equal aspect ratio,
    removes frame and ticks, and establishes normalized coordinate limits.

    Parameters
    ----------
    ax : matplotlib.axes.Axes or None
        Existing axes to configure, or None to create new axes
    figsize : tuple of float
        Figure size as (width, height) in inches, used only when creating new axes

    Returns
    -------
    matplotlib.axes.Axes
        Configured axes ready for Venn diagram plotting

    Examples
    --------
    >>> ax = init_axes(None, figsize=(8, 8))
    >>> # Or with existing axes:
    >>> fig, ax = plt.subplots()
    >>> ax = init_axes(ax, figsize=(8, 8))
    """
    if ax is None:
        _, ax = subplots(nrows=1, ncols=1, figsize=figsize)
    ax.set(
        aspect="equal",
        frame_on=False,
        xlim=(-.05, 1.05),
        ylim=(-.05, 1.05),
        xticks=[],
        yticks=[]
    )
    return ax
