"""
Dynamic geometry generation for Venn diagrams.

This module generates Venn diagram geometry dynamically using parametric equations
for circles and ellipses, similar to the ggvenn R package approach.

Based on the geometry approach from ggvenn by yanlinlin82:
https://github.com/yanlinlin82/ggvenn/blob/main/R/venn_geometry.R
"""

import numpy as np
from typing import Tuple, Dict, List
from dataclasses import dataclass


@dataclass
class Circle:
    """
    Represents a circle or ellipse in the Venn diagram.

    Attributes
    ----------
    x_offset : float
        X-coordinate of the center
    y_offset : float
        Y-coordinate of the center
    radius_a : float
        Horizontal radius (width)
    radius_b : float
        Vertical radius (height)
    theta_offset : float
        Rotation angle in radians
    """
    x_offset: float
    y_offset: float
    radius_a: float
    radius_b: float
    theta_offset: float

    def generate_points(self, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate points along the circle/ellipse perimeter.

        Uses parametric equations with rotation:
        x = x_offset + radius_a * cos(theta) * cos(theta_offset) - radius_b * sin(theta) * sin(theta_offset)
        y = y_offset + radius_a * cos(theta) * sin(theta_offset) + radius_b * sin(theta) * cos(theta_offset)

        Parameters
        ----------
        n_points : int
            Number of points to generate

        Returns
        -------
        x, y : np.ndarray, np.ndarray
            Arrays of x and y coordinates
        """
        theta = np.linspace(0, 2 * np.pi, n_points)

        # Parametric circle/ellipse
        x_raw = self.radius_a * np.cos(theta)
        y_raw = self.radius_b * np.sin(theta)

        # Apply rotation
        cos_rot = np.cos(self.theta_offset)
        sin_rot = np.sin(self.theta_offset)

        x = self.x_offset + x_raw * cos_rot - y_raw * sin_rot
        y = self.y_offset + x_raw * sin_rot + y_raw * cos_rot

        return x, y


def generate_circle_2() -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Generate geometry for 2-way Venn diagram.

    Two circles with horizontal overlap.

    Returns
    -------
    circles : List[Circle]
        List of Circle objects
    label_positions : Dict[str, Tuple[float, float]]
        Positions for intersection labels (binary logic keys)
    set_label_positions : List[Tuple[float, float]]
        Positions for set name labels
    """
    # Two circles with unit radius, horizontally aligned
    # Positioned to create proper overlap
    radius = 1.0
    x_dist = 0.75  # Distance from center to each circle center

    circles = [
        Circle(x_offset=-x_dist, y_offset=0, radius_a=radius, radius_b=radius, theta_offset=0),
        Circle(x_offset=x_dist, y_offset=0, radius_a=radius, radius_b=radius, theta_offset=0),
    ]

    # Intersection label positions (using binary logic)
    # "10" = only first set, "01" = only second set, "11" = both sets
    label_positions = {
        "10": (-x_dist - radius/2, 0),      # Left only
        "01": (x_dist + radius/2, 0),       # Right only
        "11": (0, 0),                        # Intersection
    }

    # Set name label positions (outside circles)
    set_label_positions = [
        (-x_dist, -radius - 0.3),   # Below left circle
        (x_dist, -radius - 0.3),    # Below right circle
    ]

    return circles, label_positions, set_label_positions


def generate_circle_3() -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Generate geometry for 3-way Venn diagram.

    Three circles arranged in an equilateral triangle pattern.
    Uses the same approach as ggvenn R package.

    Returns
    -------
    circles : List[Circle]
        List of Circle objects
    label_positions : Dict[str, Tuple[float, float]]
        Positions for intersection labels (binary logic keys)
    set_label_positions : List[Tuple[float, float]]
        Positions for set name labels
    """
    # Circle arrangement from ggvenn
    # Equilateral triangle with proper overlaps
    sqrt3 = np.sqrt(3)

    circles = [
        # Top left circle
        Circle(x_offset=-2/3, y_offset=(sqrt3 + 2)/6, radius_a=1.0, radius_b=1.0, theta_offset=0),
        # Top right circle
        Circle(x_offset=2/3, y_offset=(sqrt3 + 2)/6, radius_a=1.0, radius_b=1.0, theta_offset=0),
        # Bottom circle
        Circle(x_offset=0, y_offset=-(sqrt3 + 2)/6, radius_a=1.0, radius_b=1.0, theta_offset=0),
    ]

    # Intersection label positions
    # Binary logic: "100" = only first, "010" = only second, "001" = only third
    # "110" = first+second, "101" = first+third, "011" = second+third, "111" = all three
    label_positions = {
        "100": (-1.2, (sqrt3 + 2)/6),           # Left only
        "010": (1.2, (sqrt3 + 2)/6),            # Right only
        "001": (0, -(sqrt3 + 2)/6 - 0.7),       # Bottom only
        "110": (0, (sqrt3 + 2)/6 + 0.4),        # Top intersection
        "101": (-0.5, -0.2),                     # Left-bottom intersection
        "011": (0.5, -0.2),                      # Right-bottom intersection
        "111": (0, 0.1),                         # Center (all three)
    }

    # Set name label positions (outside circles)
    set_label_positions = [
        (-1.3, (sqrt3 + 2)/6 + 1.1),    # Above left circle
        (1.3, (sqrt3 + 2)/6 + 1.1),     # Above right circle
        (0, -(sqrt3 + 2)/6 - 1.3),      # Below bottom circle
    ]

    return circles, label_positions, set_label_positions


def generate_circle_4() -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Generate geometry for 4-way Venn diagram.

    Four ellipses arranged with rotation to create all intersections.
    Uses the same approach as ggvenn R package.

    Returns
    -------
    circles : List[Circle]
        List of Circle (ellipse) objects
    label_positions : Dict[str, Tuple[float, float]]
        Positions for intersection labels (binary logic keys)
    set_label_positions : List[Tuple[float, float]]
        Positions for set name labels
    """
    # Four ellipses with rotation
    # Following ggvenn geometry

    circles = [
        Circle(x_offset=-0.7, y_offset=-0.5, radius_a=0.75, radius_b=1.5, theta_offset=np.pi/4),
        Circle(x_offset=-0.7, y_offset=0.5, radius_a=0.75, radius_b=1.5, theta_offset=-np.pi/4),
        Circle(x_offset=0.7, y_offset=0.5, radius_a=0.75, radius_b=1.5, theta_offset=np.pi/4),
        Circle(x_offset=0.7, y_offset=-0.5, radius_a=0.75, radius_b=1.5, theta_offset=-np.pi/4),
    ]

    # Intersection label positions for 4-way Venn
    # Binary logic: "1000", "0100", "0010", "0001" for individual sets
    label_positions = {
        "1000": (-1.5, -0.5),       # Left-bottom only
        "0100": (-1.5, 0.5),        # Left-top only
        "0010": (1.5, 0.5),         # Right-top only
        "0001": (1.5, -0.5),        # Right-bottom only
        "1100": (-1.1, 0),          # Left two
        "0110": (-0.5, 1.0),        # Top two
        "0011": (1.1, 0),           # Right two
        "1001": (-0.5, -1.0),       # Bottom two
        "1010": (-0.3, -0.3),       # Diagonal LB-RT
        "0101": (-0.3, 0.3),        # Diagonal LT-RB
        "1110": (-0.7, 0.3),        # Left three (LB, LT, RT)
        "1101": (-0.7, -0.3),       # LB, LT, RB
        "1011": (-0.3, -0.7),       # LB, RT, RB
        "0111": (0.3, 0.3),         # LT, RT, RB
        "1111": (0, 0),             # All four
    }

    # Set name label positions (outside ellipses)
    set_label_positions = [
        (-1.2, -1.3),   # Below left-bottom ellipse
        (-1.2, 1.3),    # Above left-top ellipse
        (1.2, 1.3),     # Above right-top ellipse
        (1.2, -1.3),    # Below right-bottom ellipse
    ]

    return circles, label_positions, set_label_positions


def generate_circle_5() -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Generate geometry for 5-way Venn diagram.

    Five ellipses arranged in a pentagonal pattern with rotation.
    Based on ggvenn R package implementation.

    Returns
    -------
    circles : List[Circle]
        List of Circle (ellipse) objects
    label_positions : Dict[str, Tuple[float, float]]
        Positions for intersection labels (binary logic keys)
    set_label_positions : List[Tuple[float, float]]
        Positions for set name labels
    """
    # Five ellipses in pentagonal arrangement
    # Following ggvenn geometry

    circles = [
        Circle(x_offset=0, y_offset=0.55, radius_a=1.13, radius_b=0.64, theta_offset=np.radians(0)),
        Circle(x_offset=0.53, y_offset=-0.12, radius_a=1.13, radius_b=0.64, theta_offset=np.radians(72)),
        Circle(x_offset=0.33, y_offset=-0.60, radius_a=1.13, radius_b=0.64, theta_offset=np.radians(144)),
        Circle(x_offset=-0.33, y_offset=-0.60, radius_a=1.13, radius_b=0.64, theta_offset=np.radians(216)),
        Circle(x_offset=-0.53, y_offset=-0.12, radius_a=1.13, radius_b=0.64, theta_offset=np.radians(288)),
    ]

    # Intersection label positions for 5-way Venn
    # This is complex with 31 possible intersections (2^5 - 1)
    # Approximate positions - these may need fine-tuning
    label_positions = {
        # Single sets
        "10000": (0, 1.2),
        "01000": (0.9, 0.3),
        "00100": (0.7, -0.9),
        "00010": (-0.7, -0.9),
        "00001": (-0.9, 0.3),

        # Two-way intersections
        "11000": (0.5, 0.7),
        "01100": (0.9, -0.3),
        "00110": (0.3, -0.9),
        "00011": (-0.3, -0.9),
        "10001": (-0.5, 0.7),
        "10100": (0.4, 0.1),
        "01010": (0.4, -0.5),
        "00101": (0, -0.8),
        "10010": (-0.4, 0.1),
        "01001": (-0.4, -0.5),

        # Three-way intersections
        "11100": (0.6, 0.2),
        "01110": (0.5, -0.5),
        "00111": (0, -0.7),
        "10011": (-0.5, 0.2),
        "11001": (-0.6, -0.5),
        "11010": (0.2, 0.4),
        "01101": (0.5, -0.2),
        "00110": (0.2, -0.6),
        "10110": (-0.2, -0.2),
        "11000": (-0.2, 0.4),

        # Four-way intersections
        "11110": (0.3, 0.1),
        "01111": (0.2, -0.4),
        "10111": (-0.2, -0.3),
        "11011": (-0.3, 0.1),
        "11101": (0.1, -0.1),

        # All five
        "11111": (0, 0),
    }

    # Set name label positions (outside ellipses)
    set_label_positions = [
        (0, 1.5),       # Top
        (1.2, 0.5),     # Upper right
        (1.0, -1.2),    # Lower right
        (-1.0, -1.2),   # Lower left
        (-1.2, 0.5),    # Upper left
    ]

    return circles, label_positions, set_label_positions


def get_geometry(n_sets: int) -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Get geometry for n-way Venn diagram.

    Parameters
    ----------
    n_sets : int
        Number of sets (2-5)

    Returns
    -------
    circles : List[Circle]
        List of Circle objects defining the ellipses
    label_positions : Dict[str, Tuple[float, float]]
        Positions for intersection labels (binary logic keys)
    set_label_positions : List[Tuple[float, float]]
        Positions for set name labels

    Raises
    ------
    ValueError
        If n_sets is not between 2 and 5
    """
    geometry_functions = {
        2: generate_circle_2,
        3: generate_circle_3,
        4: generate_circle_4,
        5: generate_circle_5,
    }

    if n_sets not in geometry_functions:
        raise ValueError(f"Venn diagrams support 2-5 sets, got {n_sets}")

    return geometry_functions[n_sets]()


def normalize_coordinates(
    coords: Tuple[float, float],
    x_range: Tuple[float, float],
    y_range: Tuple[float, float],
    padding: float = 0.05
) -> Tuple[float, float]:
    """
    Normalize coordinates from raw geometry to 0-1 range for matplotlib.

    Parameters
    ----------
    coords : Tuple[float, float]
        Raw (x, y) coordinates
    x_range : Tuple[float, float]
        (min, max) of x coordinates in raw space
    y_range : Tuple[float, float]
        (min, max) of y coordinates in raw space
    padding : float
        Padding to add around the diagram (in normalized units)

    Returns
    -------
    normalized_coords : Tuple[float, float]
        Normalized (x, y) coordinates in 0-1 range
    """
    x, y = coords
    x_min, x_max = x_range
    y_min, y_max = y_range

    # Calculate range
    x_width = x_max - x_min
    y_height = y_max - y_min

    # Normalize to 0-1, leaving room for padding
    x_norm = padding + (x - x_min) / x_width * (1 - 2 * padding)
    y_norm = padding + (y - y_min) / y_height * (1 - 2 * padding)

    return x_norm, y_norm


def get_coordinate_ranges(circles: List[Circle]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Calculate the bounding box of all circles.

    Parameters
    ----------
    circles : List[Circle]
        List of Circle objects

    Returns
    -------
    x_range, y_range : Tuple[float, float], Tuple[float, float]
        (min, max) ranges for x and y coordinates
    """
    x_min = float('inf')
    x_max = float('-inf')
    y_min = float('inf')
    y_max = float('-inf')

    for circle in circles:
        # Approximate bounding box (works for small rotations)
        # For exact bounds, would need to check rotated ellipse extrema
        x_extent = max(circle.radius_a, circle.radius_b)
        y_extent = max(circle.radius_a, circle.radius_b)

        x_min = min(x_min, circle.x_offset - x_extent)
        x_max = max(x_max, circle.x_offset + x_extent)
        y_min = min(y_min, circle.y_offset - y_extent)
        y_max = max(y_max, circle.y_offset + y_extent)

    return (x_min, x_max), (y_min, y_max)
