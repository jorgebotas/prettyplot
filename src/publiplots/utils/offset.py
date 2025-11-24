from typing import List
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.transforms as transforms
from typing import Literal

def offset_lines(
    lines: List[Line2D],
    offset: float,
    orientation: Literal["vertical", "horizontal"],
) -> None:
    """
    Offset lines by a given amount.
    """
    for line in lines:
        if orientation == "vertical":
            line.set_xdata(line.get_xdata() + offset)
        else:
            line.set_ydata(line.get_ydata() + offset)

def offset_patches(
    patches: List[Patch],
    offset: float,
    orientation: Literal["vertical", "horizontal"],
) -> None:
    """
    Offset patches by a given amount.
    """
    for patch in patches:
        path = patch.get_path()
        if orientation == "vertical":
            path.vertices[:, 0] += offset
        else:
            path.vertices[:, 1] += offset
        
def offset_collections(
    collections: List[PathCollection],
    offset: float,
    ax: Axes,
    orientation: Literal["vertical", "horizontal"],
) -> None:
    """
    Offset collections by a given amount.
    """
    fig = ax.figure
    
    if orientation == 'vertical':
        # Offset in x-direction
        display_points = ax.transData.transform([(0, 0), (1, 0)])
        pixels_per_unit = display_points[1, 0] - display_points[0, 0]
        display_offset = offset * pixels_per_unit
        offset = transforms.ScaledTranslation(display_offset/fig.dpi, 0, fig.dpi_scale_trans)
    else:  # horizontal
        # Offset in y-direction
        display_points = ax.transData.transform([(0, 0), (0, 1)])
        pixels_per_unit = display_points[1, 1] - display_points[0, 1]
        display_offset = offset * pixels_per_unit
        offset = transforms.ScaledTranslation(0, display_offset/fig.dpi, fig.dpi_scale_trans)
    
    for collection in collections:
        collection.set_transform(collection.get_transform() + offset)