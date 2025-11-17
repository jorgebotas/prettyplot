"""
Constants for Venn diagram layouts.

DEPRECATED: This module previously contained precomputed normalized coordinates.
The Venn diagram implementation has been re-engineered to use dynamic geometry
calculation based on the ggvenn R package approach.

All coordinate data is now generated dynamically in the geometry.py module,
which uses raw coordinates and proper geometric calculations rather than
precomputed normalized values.

For the new implementation, see:
- geometry.py: Dynamic circle/ellipse generation with parametric equations
- diagram.py: Updated to use dynamic geometry

Based on ggvenn by yanlinlin82: https://github.com/yanlinlin82/ggvenn
"""

# This file is kept for backward compatibility but no longer contains
# the precomputed coordinate dictionaries. All geometry is now calculated
# dynamically in the geometry.py module.
