"""
Base default values for publiplots.

This module defines the fundamental default parameter values shared across
all styles. Individual styles (notebook, publication) compose these base
defaults with their specific overrides.
"""

# =============================================================================
# Matplotlib Base Defaults
# =============================================================================

MATPLOTLIB_DEFAULTS = {
    # Figure settings - compact by default (publication-ready)
    "figure.figsize": [3.5, 2.5],
    "figure.dpi": 100,
    "figure.facecolor": "white",
    "figure.edgecolor": "white",

    # Font settings - optimized for readability
    "font.size": 8,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica", "sans-serif"],

    # Axes settings
    "axes.linewidth": 1.0,
    "axes.edgecolor": "black",
    "axes.facecolor": "white",
    "axes.labelsize": 8,
    "axes.titlesize": 9,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,

    # Line settings
    "lines.linewidth": 1.5,
    "lines.markersize": 6,

    # Tick settings
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "xtick.major.size": 3,
    "ytick.major.size": 3,

    # Grid settings
    "grid.linewidth": 0.8,
    "grid.alpha": 0.3,

    # Legend settings
    "legend.fontsize": 7,
    "legend.frameon": True,
    "legend.framealpha": 0.8,
    "legend.facecolor": "white",
    "legend.edgecolor": "gray",

    # Save settings - high quality for publications
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
    "savefig.facecolor": "white",
    "savefig.edgecolor": "white",
}

# =============================================================================
# PubliPlots Custom Defaults
# =============================================================================

CUSTOM_DEFAULTS = {
    # Color and transparency
    "color": "#5d83c3",  # Default blue
    "alpha": 0.1,  # Default transparency for bars

    # Error bars
    "capsize": 0.1,  # Error bar cap size

    # Color palettes
    "palette": "pastel_categorical",  # Default color palette

    # Hatch patterns
    "hatch_mode": 1,  # Default hatch density mode (1=sparse)
}
