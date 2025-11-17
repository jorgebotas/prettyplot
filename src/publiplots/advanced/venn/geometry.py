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


def generate_circle_2(overlap_size: float = 0.5) -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Generate geometry for 2-way Venn diagram.

    Two circles with horizontal overlap.
    Uses the exact formula from ggvenn R package.

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
    # Using R's formula: x_dist = (a_radius + b_radius - overlap_size * 2) / 2
    # Default overlap_size = 0.5 for larger, more visible intersections
    a_radius = 1.0
    b_radius = 1.0
    x_dist = (a_radius + b_radius - overlap_size * 2) / 2

    circles = [
        Circle(x_offset=-x_dist, y_offset=0, radius_a=a_radius, radius_b=a_radius, theta_offset=0),
        Circle(x_offset=x_dist, y_offset=0, radius_a=b_radius, radius_b=b_radius, theta_offset=0),
    ]

    # Intersection label positions (using binary logic)
    # "10" = only first set, "01" = only second set, "11" = both sets
    label_positions = {
        "10": (-x_dist - a_radius/2, 0),      # Left only
        "01": (x_dist + b_radius/2, 0),       # Right only
        "11": (0, 0),                          # Intersection
    }

    # Set name label positions (outside circles)
    set_label_positions = [
        (-x_dist, -a_radius - 0.3),   # Below left circle
        (x_dist, -b_radius - 0.3),    # Below right circle
    ]

    return circles, label_positions, set_label_positions


def generate_circle_3(radius_scale: float = 1.3) -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Generate geometry for 3-way Venn diagram.

    Three circles arranged in an equilateral triangle pattern.
    Based on ggvenn R package geometry with increased radius for better visibility.

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
    # Equilateral triangle with scaled radius for larger, more visible intersections
    # Default radius_scale = 1.3
    sqrt3 = np.sqrt(3)
    base_radius = 1.0 * radius_scale

    circles = [
        # Top left circle
        Circle(x_offset=-2/3, y_offset=(sqrt3 + 2)/6, radius_a=base_radius, radius_b=base_radius, theta_offset=0),
        # Top right circle
        Circle(x_offset=2/3, y_offset=(sqrt3 + 2)/6, radius_a=base_radius, radius_b=base_radius, theta_offset=0),
        # Bottom circle
        Circle(x_offset=0, y_offset=-(sqrt3 + 2)/6, radius_a=base_radius, radius_b=base_radius, theta_offset=0),
    ]

    # Intersection label positions
    # Binary logic: "100" = only first, "010" = only second, "001" = only third
    # "110" = first+second, "101" = first+third, "011" = second+third, "111" = all three
    # Adjust bottom intersection positions based on radius scale
    bottom_intersection_y = -0.2 - (radius_scale - 1.0) * 0.5

    label_positions = {
        "100": (-1.2, (sqrt3 + 2)/6 + 0.2),           # Left only
        "010": (1.2, (sqrt3 + 2)/6 + 0.2),            # Right only
        "001": (0, -(sqrt3 + 2)/6 - 0.7),       # Bottom only
        "110": (0, (sqrt3 + 2)/6 + 0.4),        # Top intersection
        "101": (-0.8, bottom_intersection_y),   # Left-bottom intersection (adjusted for radius)
        "011": (0.8, bottom_intersection_y),    # Right-bottom intersection (adjusted for radius)
        "111": (0, 0.1),                         # Center (all three)
    }

    # Set name label positions (outside circles)
    # Adjust based on radius scale
    label_offset = base_radius + 0.3
    set_label_positions = [
        (-1.3, (sqrt3 + 2)/6 + label_offset),    # Above left circle
        (1.3, (sqrt3 + 2)/6 + label_offset),     # Above right circle
        (0, -(sqrt3 + 2)/6 - label_offset),      # Below bottom circle
    ]

    return circles, label_positions, set_label_positions


def generate_circle_4() -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Generate geometry for 4-way Venn diagram.

    Four ellipses arranged with rotation to create all intersections.
    Uses exact coordinates from ggvenn R package.

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
    # Exact coordinates from ggvenn gen_circle_4:
    # gen_circle(1L, -.7, -1/2, .75, 1.5, pi/4),
    # gen_circle(2L, -.72+2/3, -1/6, .75, 1.5, pi/4),
    # gen_circle(3L, .72-2/3, -1/6, .75, 1.5, -pi/4),
    # gen_circle(4L, .7, -1/2, .75, 1.5, -pi/4)

    circles = [
        Circle(x_offset=-0.7, y_offset=-1/2, radius_a=0.75, radius_b=1.5, theta_offset=np.pi/4),
        Circle(x_offset=-0.72+2/3, y_offset=-1/6, radius_a=0.75, radius_b=1.5, theta_offset=np.pi/4),
        Circle(x_offset=0.72-2/3, y_offset=-1/6, radius_a=0.75, radius_b=1.5, theta_offset=-np.pi/4),
        Circle(x_offset=0.7, y_offset=-1/2, radius_a=0.75, radius_b=1.5, theta_offset=-np.pi/4),
    ]

    # Intersection label positions from gen_text_pos_4
    # Converting R labels (A, B, C, D) to binary logic (1000, 0100, 0010, 0001)
    label_positions = {
        # Individual sets
        "1000": (-1.5, 0.0),        # A
        "0100": (-0.6, 0.7),        # B
        "0010": (0.6, 0.7),         # C
        "0001": (1.5, 0.0),         # D
        # Two-way intersections
        "1100": (-0.9, 0.3),        # AB
        "0110": (0.0, 0.4),         # BC
        "0011": (0.9, 0.3),         # CD
        "1010": (-0.8, -0.9),       # AC
        "0101": (0.8, -0.9),        # BD
        "1001": (0.0, -1.4),        # AD
        # Three-way intersections
        "1110": (-0.5, -0.2),       # ABC
        "0111": (0.5, -0.2),        # BCD
        "1011": (-0.3, -1.1),       # ACD
        "1101": (0.3, -1.1),        # ABD
        # All four
        "1111": (0.0, -0.7),        # ABCD
    }

    # Set name label positions (outside ellipses)
    set_label_positions = [
        (-1.5, 0.0),    # A (left)
        (-0.6, 0.7),    # B (upper left)
        (0.6, 0.7),     # C (upper right)
        (1.5, 0.0),     # D (right)
    ]

    return circles, label_positions, set_label_positions


def _label_name_to_binary(name: str, n_sets: int = 5) -> str:
    """
    Convert R-style label name (e.g., 'ABC') to binary logic (e.g., '11100').

    Parameters
    ----------
    name : str
        Label name using letters A, B, C, D, E
    n_sets : int
        Total number of sets (default 5)

    Returns
    -------
    binary : str
        Binary string representation
    """
    if name == "-" or name == "ABCDE":
        return "11111" if name == "ABCDE" else "-"

    result = ['0'] * n_sets
    for char in name:
        idx = ord(char) - ord('A')
        if idx < n_sets:
            result[idx] = '1'
    return ''.join(result)


def _gen_label_pos_list(name_list: List[str], radius: float, start_angle: float, n_sets: int = 5) -> Dict[str, Tuple[float, float]]:
    """
    Generate label positions in a circular arrangement.

    Mimics R's gen_label_pos_list function.
    """
    n = len(name_list)
    positions = {}

    for i, name in enumerate(name_list):
        theta = start_angle + i * 2 * np.pi / n
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        binary = _label_name_to_binary(name, n_sets)
        if binary != "-":
            positions[binary] = (x, y)

    return positions


def generate_circle_5() -> Tuple[List[Circle], Dict[str, Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Generate geometry for 5-way Venn diagram.

    Five ellipses arranged in a pentagonal pattern with rotation.
    Uses exact coordinates from ggvenn R package.

    Returns
    -------
    circles : List[Circle]
        List of Circle (ellipse) objects
    label_positions : Dict[str, Tuple[float, float]]
        Positions for intersection labels (binary logic keys)
    set_label_positions : List[Tuple[float, float]]
        Positions for set name labels
    """
    # Five ellipses using gen_circle_list parameters:
    # gen_circle_list(5, 1, 3.1, 1.5, pi * 0.45, pi * 0.1)
    # center_radius = 1, ellipse_a = 3.1, ellipse_b = 1.5
    # start_angle = 0.45π, rotation_offset = 0.1π

    circles = []
    n = 5
    center_radius = 1.0
    ellipse_a = 3.1
    ellipse_b = 1.5
    start_angle = np.pi * 0.45
    rotation_offset = np.pi * 0.1

    for i in range(n):
        theta = start_angle + 2 * np.pi * i / n
        x = center_radius * np.cos(theta)
        y = center_radius * np.sin(theta)
        rotation = theta + rotation_offset
        circles.append(Circle(
            x_offset=x,
            y_offset=y,
            radius_a=ellipse_a,
            radius_b=ellipse_b,
            theta_offset=rotation
        ))

    # Generate label positions using gen_text_pos_5 logic
    label_positions = {}

    # Center: ABCDE
    label_positions["11111"] = (0.0, 0.0)

    # Four-way intersections (radius 1.42, start 1.12π)
    label_positions.update(_gen_label_pos_list(
        ["BCDE", "ACDE", "ABDE", "ABCE", "ABCD"],
        radius=1.42, start_angle=np.pi * 1.12, n_sets=5
    ))

    # Three-way intersections - first ring (radius 1.55, start 1.33π)
    label_positions.update(_gen_label_pos_list(
        ["CDE", "ADE", "ABE", "ABC", "BCD"],
        radius=1.55, start_angle=np.pi * 1.33, n_sets=5
    ))

    # Three-way intersections - second ring (radius 1.88, start 1.13π)
    label_positions.update(_gen_label_pos_list(
        ["BCE", "ACD", "BDE", "ACE", "ABD"],
        radius=1.88, start_angle=np.pi * 1.13, n_sets=5
    ))

    # Two-way intersections - first ring (radius 1.98, start 0.44π)
    label_positions.update(_gen_label_pos_list(
        ["AC", "BD", "CE", "AD", "BE"],
        radius=1.98, start_angle=np.pi * 0.44, n_sets=5
    ))

    # Two-way intersections - second ring (radius 2.05, start 0.68π)
    label_positions.update(_gen_label_pos_list(
        ["AB", "BC", "CD", "DE", "AE"],
        radius=2.05, start_angle=np.pi * 0.68, n_sets=5
    ))

    # Single sets (radius 3.0, start 0.52π)
    label_positions.update(_gen_label_pos_list(
        ["A", "B", "C", "D", "E"],
        radius=3.0, start_angle=np.pi * 0.52, n_sets=5
    ))

    # Set name label positions (same as individual set positions)
    set_label_positions = []
    for name in ["A", "B", "C", "D", "E"]:
        binary = _label_name_to_binary(name, 5)
        set_label_positions.append(label_positions[binary])

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
    if n_sets == 2:
        return generate_circle_2()
    elif n_sets == 3:
        return generate_circle_3()
    elif n_sets == 4:
        return generate_circle_4()
    elif n_sets == 5:
        return generate_circle_5()
    else:
        raise ValueError(f"Venn diagrams support 2-5 sets, got {n_sets}")


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
