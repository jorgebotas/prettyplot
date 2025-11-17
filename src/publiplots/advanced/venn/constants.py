"""
Constants for Venn diagram layouts.

This module contains the coordinate data and parameters for rendering Venn diagrams
with 2 to 5 sets. The data defines the positions, dimensions, and angles for the
ellipses as well as the positions for the petal labels showing intersection sizes
and the set labels displayed outside each set's shape.

Adapted from pyvenn by LankyCyril (https://github.com/LankyCyril/pyvenn)
"""

# Coordinates for the centers of shapes (ellipses)
# For 2-5 sets: (x, y) tuples for ellipse centers
SHAPE_COORDS = {
    2: [(.375, .500), (.625, .500)],
    3: [(.400, .600), (.600, .600), (.500, .420)],
    4: [(.350, .400), (.450, .500), (.544, .500), (.644, .400)],
    5: [(.428, .449), (.469, .543), (.558, .523), (.578, .432), (.489, .383)],
    6: [
        (.637, .921, .649, .274, .188, .667),
        (.981, .769, .335, .191, .393, .671),
        (.941, .397, .292, .475, .456, .747),
        (.662, .119, .316, .548, .662, .700),
        (.309, .081, .374, .718, .681, .488),
        (.016, .626, .726, .687, .522, .327)
    ]
}

# Dimensions for shapes (width, height) for ellipses
SHAPE_DIMS = {
    2: [(.50, .50), (.50, .50)],
    3: [(.50, .50), (.50, .50), (.50, .50)],
    4: [(.72, .45), (.72, .45), (.72, .45), (.72, .45)],
    5: [(.87, .50), (.87, .50), (.87, .50), (.87, .50), (.87, .50)],
    6: [(None,)] * 6
}

# Rotation angles for ellipses (in degrees)
SHAPE_ANGLES = {
    2: [0, 0],
    3: [0, 0, 0],
    4: [140, 140, 40, 40],
    5: [155, 82, 10, 118, 46],
    6: [None] * 6
}

# Coordinates for petal labels showing intersection sizes
# Keys are binary strings representing which sets are included (e.g., "101" = sets 0 and 2)
# Values are (x, y) tuples for label positions
PETAL_LABEL_COORDS = {
    2: {
        "01": (.74, .50), "10": (.26, .50), "11": (.50, .50)
    },
    3: {

        "001": (.500, .220), "010": (.760, .680), "011": (.660, .430),
        "100": (.240, .680), "101": (.320, .430), "110": (.500, .720),
        "111": (.500, .520)

    },
    4: {
        "0001": (.85, .42), "0010": (.68, .72), "0011": (.77, .59),
        "0100": (.32, .72), "0101": (.71, .30), "0110": (.50, .66),
        "0111": (.65, .50), "1000": (.14, .42), "1001": (.50, .17),
        "1010": (.29, .30), "1011": (.39, .24), "1100": (.23, .59),
        "1101": (.61, .24), "1110": (.35, .50), "1111": (.50, .38)
    },
    5: {
        "00001": (.27, .11), "00010": (.72, .11), "00011": (.55, .13),
        "00100": (.91, .58), "00101": (.78, .64), "00110": (.84, .41),
        "00111": (.76, .55), "01000": (.51, .90), "01001": (.39, .15),
        "01010": (.42, .78), "01011": (.50, .15), "01100": (.67, .76),
        "01101": (.70, .71), "01110": (.51, .74), "01111": (.64, .67),
        "10000": (.10, .61), "10001": (.20, .31), "10010": (.76, .25),
        "10011": (.65, .23), "10100": (.18, .50), "10101": (.21, .37),
        "10110": (.81, .37), "10111": (.74, .40), "11000": (.27, .70),
        "11001": (.34, .25), "11010": (.33, .72), "11011": (.51, .22),
        "11100": (.25, .58), "11101": (.28, .39), "11110": (.36, .66),
        "11111": (.51, .47)
    },

}


# Coordinates for set labels (displayed outside each set's shape)
# Positioned to be clearly outside the circles/ellipses for readability
SET_LABEL_COORDS = {
    # 2 sets: Below circles at same x-coordinate
    2: [
        (.375, .20),   # Set 0: Below left circle
        (.625, .20)    # Set 1: Below right circle
    ],
    # 3 sets: Outside circle radius
    3: [
        (.300, .88),   # Set 0: Above top-left circle
        (.700, .88),   # Set 1: Above top-right circle
        (.500, .12)    # Set 2: Below bottom circle
    ],
    # 4 sets: Top two above, bottom two below ellipses
    4: [
        (.356, .10),   # Set 0: Below left ellipse
        (.356, .80),   # Set 1: Above top-left ellipse
        (.644, .80),   # Set 2: Above top-right ellipse
        (.644, .10)    # Set 3: Below right ellipse
    ],
    # 5 sets: At outer edges of ellipse arrangement
    5: [
        (.20, .75),    # Set 0: Upper left outer edge
        (.50, .98),    # Set 2: Upper center outer edge
        (.80, .75),    # Set 3: Upper right outer edge
        (.80, .00),    # Set 4: Lower right outer edge
        (.20, .00)     # Set 4: Lower left outer edge
    ],
}

# Text alignment for set labels (horizontal, vertical)
# Alignment is chosen based on label position relative to shapes:
# - Labels above shapes: va="bottom" (text extends down toward shape)
# - Labels below shapes: va="top" (text extends up toward shape)
# - Labels left of shapes: ha="right" (text extends right toward shape)
# - Labels right of shapes: ha="left" (text extends left toward shape)
SET_LABEL_ALIGNMENTS = {
    # 2 sets: Both labels below circles
    2: [
        ("right", "top"),     # Set 0: Below left circle
        ("left", "top")       # Set 1: Below right circle
    ],
    # 3 sets: Two above, one below
    3: [
        ("right", "bottom"),  # Set 0: Above top-left circle
        ("left", "bottom"),   # Set 1: Above top-right circle
        ("center", "top")     # Set 2: Below bottom circle
    ],
    # 4 sets: Bottom two below, top two above ellipses
    4: [
        ("right", "top"),     # Set 0: Below left ellipse
        ("right", "bottom"),  # Set 1: Above top-left ellipse
        ("left", "bottom"),   # Set 2: Above top-right ellipse
        ("left", "top")       # Set 3: Below right ellipse
    ],
    # 5 sets: Mixed positioning at outer edges
    5: [
        ("right", "bottom"),  # Set 0: Above and left of upper-left ellipse
        ("center", "bottom"), # Set 1: Above top ellipse
        ("left", "bottom"),   # Set 2: Above and right of upper-right ellipse
        ("left", "center"),   # Set 3: Right of lower-right ellipse
        ("right", "center")   # Set 4: Left of lower-left ellipse
    ],
}
