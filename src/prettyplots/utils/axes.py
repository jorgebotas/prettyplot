"""
Axis manipulation utilities for prettyplots.

This module provides functions for manipulating axes appearance,
including spines, grids, labels, and limits.
"""

from typing import Optional, List, Union, Tuple
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def adjust_spines(
    ax: Axes,
    spines: Union[str, List[str]] = 'left-bottom',
    color: str = '0.2',
    linewidth: float = 1.5,
    offset: Optional[float] = None
) -> None:
    """
    Adjust which spines are visible and their appearance.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    spines : str or List[str], default='left-bottom'
        Which spines to show. Can be:
        - 'all': Show all spines
        - 'none': Hide all spines
        - 'left-bottom': Show only left and bottom (default for prettyplots)
        - 'box': Show all four spines (box around plot)
        - List of spine names: ['left', 'bottom', 'right', 'top']
    color : str, default='0.2'
        Color of visible spines.
    linewidth : float, default=1.5
        Width of visible spines.
    offset : float, optional
        Offset spines from data by this amount in points.

    Examples
    --------
    Show only left and bottom spines (publication style):
    >>> pp.adjust_spines(ax, spines='left-bottom')

    Show all spines:
    >>> pp.adjust_spines(ax, spines='all')

    Hide all spines:
    >>> pp.adjust_spines(ax, spines='none')

    Custom spine selection:
    >>> pp.adjust_spines(ax, spines=['left', 'right'])
    """
    # Parse spines parameter
    if spines == 'all':
        visible_spines = ['left', 'bottom', 'right', 'top']
    elif spines == 'none':
        visible_spines = []
    elif spines == 'left-bottom':
        visible_spines = ['left', 'bottom']
    elif spines == 'box':
        visible_spines = ['left', 'bottom', 'right', 'top']
    elif isinstance(spines, list):
        visible_spines = spines
    else:
        raise ValueError(
            f"Invalid spines parameter: {spines}. "
            "Use 'all', 'none', 'left-bottom', 'box', or a list of spine names."
        )

    # Set spine visibility and properties
    for spine_name in ['left', 'bottom', 'right', 'top']:
        spine = ax.spines[spine_name]
        if spine_name in visible_spines:
            spine.set_visible(True)
            spine.set_color(color)
            spine.set_linewidth(linewidth)
            if offset is not None:
                spine.set_position(('outward', offset))
        else:
            spine.set_visible(False)

    # Adjust tick visibility
    if 'bottom' not in visible_spines:
        ax.xaxis.set_ticks_position('none')
    if 'left' not in visible_spines:
        ax.yaxis.set_ticks_position('none')


def add_grid(
    ax: Axes,
    which: str = 'major',
    axis: str = 'both',
    alpha: float = 0.3,
    linestyle: str = '--',
    linewidth: float = 0.5,
    color: str = '0.8',
    zorder: int = 0
) -> None:
    """
    Add customizable gridlines to axes.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    which : str, default='major'
        Which gridlines to show: 'major', 'minor', or 'both'.
    axis : str, default='both'
        Which axis to add grid: 'x', 'y', or 'both'.
    alpha : float, default=0.3
        Transparency of gridlines (0-1).
    linestyle : str, default='--'
        Style of gridlines.
    linewidth : float, default=0.5
        Width of gridlines.
    color : str, default='0.8'
        Color of gridlines.
    zorder : int, default=0
        Z-order of gridlines (lower values are behind other elements).

    Examples
    --------
    Add default gridlines:
    >>> pp.add_grid(ax)

    Add only horizontal gridlines:
    >>> pp.add_grid(ax, axis='y')

    Customize grid appearance:
    >>> pp.add_grid(ax, alpha=0.5, linestyle=':', color='blue')
    """
    ax.grid(
        True,
        which=which,
        axis=axis,
        alpha=alpha,
        linestyle=linestyle,
        linewidth=linewidth,
        color=color,
        zorder=zorder
    )
    ax.set_axisbelow(True)  # Ensure grid is behind data


def remove_grid(ax: Axes, axis: str = 'both') -> None:
    """
    Remove gridlines from axes.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    axis : str, default='both'
        Which axis to remove grid from: 'x', 'y', or 'both'.

    Examples
    --------
    >>> pp.remove_grid(ax)
    """
    ax.grid(False, axis=axis)


def set_axis_labels(
    ax: Axes,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
    fontsize: Optional[float] = None,
    fontweight: str = 'normal'
) -> None:
    """
    Set axis labels and title with consistent formatting.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    xlabel : str, optional
        X-axis label.
    ylabel : str, optional
        Y-axis label.
    title : str, optional
        Plot title.
    fontsize : float, optional
        Font size for labels. If None, uses current rcParams.
    fontweight : str, default='normal'
        Font weight: 'normal', 'bold', 'light', etc.

    Examples
    --------
    >>> pp.set_axis_labels(ax, xlabel='Time (s)', ylabel='Signal', title='Results')
    """
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=fontsize, fontweight=fontweight)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=fontsize, fontweight=fontweight)
    if title is not None:
        ax.set_title(title, fontsize=fontsize, fontweight=fontweight)


def set_axis_limits(
    ax: Axes,
    xlim: Optional[Tuple[float, float]] = None,
    ylim: Optional[Tuple[float, float]] = None,
    expand: float = 0.0
) -> None:
    """
    Set axis limits with optional expansion.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    xlim : Tuple[float, float], optional
        X-axis limits as (min, max).
    ylim : Tuple[float, float], optional
        Y-axis limits as (min, max).
    expand : float, default=0.0
        Fraction to expand limits beyond specified range (0-1).
        E.g., 0.1 adds 10% padding on each side.

    Examples
    --------
    Set specific limits:
    >>> pp.set_axis_limits(ax, xlim=(0, 10), ylim=(0, 100))

    Set limits with padding:
    >>> pp.set_axis_limits(ax, xlim=(0, 10), expand=0.05)
    """
    if xlim is not None:
        x_min, x_max = xlim
        if expand > 0:
            x_range = x_max - x_min
            x_min -= x_range * expand
            x_max += x_range * expand
        ax.set_xlim(x_min, x_max)

    if ylim is not None:
        y_min, y_max = ylim
        if expand > 0:
            y_range = y_max - y_min
            y_min -= y_range * expand
            y_max += y_range * expand
        ax.set_ylim(y_min, y_max)


def rotate_xticklabels(
    ax: Axes,
    rotation: float = 45,
    ha: str = 'right',
    va: str = 'top'
) -> None:
    """
    Rotate x-axis tick labels.

    Commonly used when labels are long or numerous.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    rotation : float, default=45
        Rotation angle in degrees.
    ha : str, default='right'
        Horizontal alignment: 'left', 'center', 'right'.
    va : str, default='top'
        Vertical alignment: 'top', 'center', 'bottom', 'baseline'.

    Examples
    --------
    >>> pp.rotate_xticklabels(ax, rotation=45)
    >>> pp.rotate_xticklabels(ax, rotation=90, ha='right')
    """
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=rotation,
        ha=ha,
        va=va
    )


def rotate_yticklabels(
    ax: Axes,
    rotation: float = 0,
    ha: str = 'right',
    va: str = 'center'
) -> None:
    """
    Rotate y-axis tick labels.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    rotation : float, default=0
        Rotation angle in degrees.
    ha : str, default='right'
        Horizontal alignment: 'left', 'center', 'right'.
    va : str, default='center'
        Vertical alignment: 'top', 'center', 'bottom'.

    Examples
    --------
    >>> pp.rotate_yticklabels(ax, rotation=45)
    """
    ax.set_yticklabels(
        ax.get_yticklabels(),
        rotation=rotation,
        ha=ha,
        va=va
    )


def invert_axis(ax: Axes, axis: str = 'y') -> None:
    """
    Invert an axis direction.

    Useful for heatmaps or other visualizations where reversed order
    is more intuitive.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    axis : str, default='y'
        Which axis to invert: 'x' or 'y'.

    Examples
    --------
    Invert y-axis (common for heatmaps):
    >>> pp.invert_axis(ax, axis='y')

    Invert x-axis:
    >>> pp.invert_axis(ax, axis='x')
    """
    if axis == 'y':
        ax.invert_yaxis()
    elif axis == 'x':
        ax.invert_xaxis()
    else:
        raise ValueError(f"Invalid axis '{axis}'. Use 'x' or 'y'.")


def add_reference_line(
    ax: Axes,
    value: float,
    axis: str = 'y',
    color: str = 'red',
    linestyle: str = '--',
    linewidth: float = 1.5,
    alpha: float = 0.7,
    label: Optional[str] = None,
    zorder: int = 1
) -> None:
    """
    Add a reference line to the plot.

    Useful for showing thresholds, means, or other reference values.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.
    value : float
        Position of the reference line.
    axis : str, default='y'
        Which axis to add line to: 'x' (vertical) or 'y' (horizontal).
    color : str, default='red'
        Line color.
    linestyle : str, default='--'
        Line style.
    linewidth : float, default=1.5
        Line width.
    alpha : float, default=0.7
        Line transparency (0-1).
    label : str, optional
        Label for legend.
    zorder : int, default=1
        Z-order (higher values are on top).

    Examples
    --------
    Add horizontal reference line at y=0:
    >>> pp.add_reference_line(ax, value=0, axis='y', label='Baseline')

    Add vertical line at x=5:
    >>> pp.add_reference_line(ax, value=5, axis='x', color='blue')
    """
    if axis == 'y':
        ax.axhline(
            y=value,
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            alpha=alpha,
            label=label,
            zorder=zorder
        )
    elif axis == 'x':
        ax.axvline(
            x=value,
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            alpha=alpha,
            label=label,
            zorder=zorder
        )
    else:
        raise ValueError(f"Invalid axis '{axis}'. Use 'x' or 'y'.")


def set_aspect_equal(ax: Axes) -> None:
    """
    Set equal aspect ratio for the axes.

    Forces x and y axes to have the same scale, useful for scatter plots
    where true distances matter.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes object.

    Examples
    --------
    >>> pp.set_aspect_equal(ax)
    """
    ax.set_aspect('equal', adjustable='box')


def tighten_layout(fig: Optional[plt.Figure] = None) -> None:
    """
    Apply tight layout to figure.

    Automatically adjusts subplot parameters to give specified padding.

    Parameters
    ----------
    fig : Figure, optional
        Matplotlib figure object. If None, uses current figure.

    Examples
    --------
    >>> pp.tighten_layout(fig)
    >>> pp.tighten_layout()  # Uses current figure
    """
    if fig is None:
        plt.tight_layout()
    else:
        fig.tight_layout()
