"""
UpSet plot module for visualizing set intersections.

This module provides functionality for creating UpSet plots, an effective
visualization technique for displaying intersections of multiple sets.

Portions of this implementation are based on concepts from UpSetPlot:
https://github.com/jnothman/UpSetPlot
Copyright (c) 2016, Joel Nothman
Licensed under BSD-3-Clause
"""

from .diagram import upsetplot

__all__ = ["upsetplot"]
