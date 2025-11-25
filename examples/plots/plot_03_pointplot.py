"""
Point Plot Examples
===================

This example demonstrates point plot functionality in PubliPlots,
showing point estimates with error bars connected by lines. Point plots
are ideal for visualizing trends across categorical variables and
comparing groups over time or conditions.
"""

import publiplots as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set style
pp.set_notebook_style()

# %%
# Simple Point Plot
# -----------------
# Basic point plot showing mean values with confidence intervals.

# Create sample data
np.random.seed(42)
simple_data = pd.DataFrame({
    'time': np.repeat(['Day 1', 'Day 2', 'Day 3', 'Day 4'], 20),
    'measurement': np.concatenate([
        np.random.normal(50, 8, 20),
        np.random.normal(55, 9, 20),
        np.random.normal(62, 10, 20),
        np.random.normal(70, 12, 20),
    ])
})

# Create simple point plot
fig, ax = pp.pointplot(
    data=simple_data,
    x='time',
    y='measurement',
    title='Simple Point Plot',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Point Plot with Custom Color
# -----------------------------
# Control the color of points and lines.

# Create point plot with custom color
fig, ax = pp.pointplot(
    data=simple_data,
    x='time',
    y='measurement',
    color='#8E8EC1',
    title='Point Plot with Custom Color',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Point Plot with Hue Grouping
# -----------------------------
# Compare multiple groups with different colors and markers.

# Create grouped data
np.random.seed(123)
hue_data = pd.DataFrame({
    'time': np.repeat(['Day 1', 'Day 2', 'Day 3', 'Day 4'], 20),
    'group': np.tile(np.repeat(['Control', 'Treated'], 10), 4),
    'measurement': np.concatenate([
        np.random.normal(50, 8, 10), np.random.normal(52, 8, 10),
        np.random.normal(52, 9, 10), np.random.normal(65, 10, 10),
        np.random.normal(54, 9, 10), np.random.normal(78, 12, 10),
        np.random.normal(55, 10, 10), np.random.normal(85, 14, 10),
    ])
})

# Create point plot with hue
fig, ax = pp.pointplot(
    data=hue_data,
    x='time',
    y='measurement',
    hue='group',
    title='Point Plot with Hue Grouping',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Point Plot with Custom Palette
# -------------------------------
# Use a custom color palette for groups.

fig, ax = pp.pointplot(
    data=hue_data,
    x='time',
    y='measurement',
    hue='group',
    palette={'Control': '#8E8EC1', 'Treated': '#75B375'},
    title='Point Plot with Custom Palette',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Point Plot with Custom Markers
# -------------------------------
# Use different marker shapes for each group.

fig, ax = pp.pointplot(
    data=hue_data,
    x='time',
    y='measurement',
    hue='group',
    markers=["o", "D"],
    palette={'Control': '#8E8EC1', 'Treated': '#75B375'},
    title='Point Plot with Custom Markers',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Point Plot with Custom Line Styles
# -----------------------------------
# Use different line styles to distinguish groups.

fig, ax = pp.pointplot(
    data=hue_data,
    x='time',
    y='measurement',
    hue='group',
    linestyles=["-", ":"],
    palette={'Control': '#8E8EC1', 'Treated': '#75B375'},
    title='Point Plot with Custom Line Styles',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Complete Customization
# ----------------------
# Combine custom markers, line styles, and palette with error bars.

fig, ax = pp.pointplot(
    data=hue_data,
    x='time',
    y='measurement',
    hue='group',
    errorbar='se',
    markers=["o", "D"],
    linestyles=["-", ":"],
    palette={'Control': '#8E8EC1', 'Treated': '#75B375'},
    title='Fully Customized Point Plot',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Point Plot with Standard Error
# -------------------------------
# Use standard error instead of confidence intervals.

fig, ax = pp.pointplot(
    data=hue_data,
    x='time',
    y='measurement',
    hue='group',
    errorbar='se',
    title='Point Plot with Standard Error',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Point Plot with Standard Deviation
# -----------------------------------
# Show standard deviation as error bars.

fig, ax = pp.pointplot(
    data=hue_data,
    x='time',
    y='measurement',
    hue='group',
    errorbar='sd',
    title='Point Plot with Standard Deviation',
    xlabel='Time Point',
    ylabel='Measurement',
)
ax.grid(axis="y", alpha=0.3)
plt.show()

# %%
# Forest Plot Example
# -------------------
# Create a forest plot showing effect sizes with confidence intervals.
# Forest plots are commonly used in meta-analyses and clinical trials.
# We use a horizontal pointplot (swap x and y) to create the forest plot.

# Create forest plot data
np.random.seed(456)
forest_data = pd.DataFrame({
    'study': [
        'Smith et al. (2020)',
        'Johnson et al. (2019)',
        'Williams et al. (2021)',
        'Brown et al. (2018)',
        'Davis et al. (2022)',
        'Miller et al. (2020)',
        'Wilson et al. (2019)',
        'Moore et al. (2021)',
    ],
    'effect_size': [0.45, 0.62, 0.38, 0.71, 0.55, 0.48, 0.59, 0.52],
})

# Create forest plot using pointplot with horizontal orientation
fig, ax = pp.pointplot(
    data=forest_data,
    x='effect_size',
    y='study',
    color='#8E8EC1',
    errorbar=('pi', 100),
    capsize=0.1,
    title='Forest Plot: Meta-Analysis of Treatment Effect',
    xlabel='Effect Size (95% CI)',
    ylabel='Study',
    figsize=(8, 6),
)

# Add vertical line at null effect
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

# %%
# Forest Plot with Subgroups
# ---------------------------
# Forest plot showing different study types or subgroups using hue.

# Create forest plot data with subgroups
np.random.seed(789)
subgroup_forest_data = pd.DataFrame({
    'study': [
        'Smith 2020',
        'Johnson 2019',
        'Williams 2021',
        'Brown 2018',
        'Davis 2022',
        'Miller 2020',
        'Wilson 2019',
        'Moore 2021',
    ],
    'type': ['RCT', 'RCT', 'RCT', 'RCT', 
             'Observational', 'Observational', 'Observational', 'Observational'],
    'effect_size': [0.45, 0.62, 0.38, 0.71, 0.35, 0.28, 0.42, 0.31],
})

# Create forest plot with hue for study types
fig, ax = pp.pointplot(
    data=subgroup_forest_data,
    x='effect_size',
    y='study',
    hue='type',
    errorbar=('pi', 100),
    capsize=0.1,
    palette={'RCT': '#75B375', 'Observational': '#8E8EC1'},
    markers=['o', 's'],
    dodge=0.3,
    title='Forest Plot: Treatment Effect by Study Type',
    xlabel='Effect Size (95% CI)',
    ylabel='Study',
    figsize=(8, 7),
)

# Add vertical line at null effect
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()
