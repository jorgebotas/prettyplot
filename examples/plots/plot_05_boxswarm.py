"""
Combined Box and Swarm Plots
============================

This example shows how to overlay swarm plots on box plots for richer
visualizations that show both distribution summary and individual data points.
"""

import publiplots as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set style
pp.set_notebook_style()

# %%
# Box Plot with Swarm Overlay
# ---------------------------
# Combining box plots with swarm plots shows both the distribution summary
# and individual data points.

# Create sample data
np.random.seed(42)
n = 120
data = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C'], n // 3),
    'value': np.concatenate([
        np.random.normal(10, 2, n // 3),
        np.random.normal(15, 3, n // 3),
        np.random.normal(12, 2.5, n // 3)
    ])
})

# Create box plot first
fig, ax = pp.boxplot(
    data=data,
    x='category',
    y='value',
    showfliers=False,  # Hide outliers since swarm will show all points
    title='Box Plot with Swarm Overlay',
    xlabel='Category',
    ylabel='Value',
)

# Overlay swarm plot with alpha=1 for better visibility
pp.swarmplot(
    data=data,
    x='category',
    y='value',
    ax=ax,
    alpha=1,  # Full opacity for swarm points
    size=4,
    legend=False
)
plt.show()

# %%
# Grouped Box Plot with Swarm Overlay
# -----------------------------------
# Combined visualization with hue grouping.

# Add group variable
data['group'] = np.tile(['Group 1', 'Group 2'], n // 2)

# Create grouped box plot
fig, ax = pp.boxplot(
    data=data,
    x='category',
    y='value',
    hue='group',
    showfliers=False,
    title='Grouped Box Plot with Swarm Overlay',
    xlabel='Category',
    ylabel='Value',
    palette={'Group 1': '#8E8EC1', 'Group 2': '#75B375'},
)

# Overlay swarm plot
pp.swarmplot(
    data=data,
    x='category',
    y='value',
    hue='group',
    dodge=True,
    ax=ax,
    alpha=1,  # Full opacity for swarm points
    size=3,
    legend=False,
    palette={'Group 1': '#8E8EC1', 'Group 2': '#75B375'},
)
plt.show()

# %%
# Box and Swarm with Different Alpha
# ----------------------------------
# Use transparent boxes with opaque swarm points.

# Create box plot with lower alpha
fig, ax = pp.boxplot(
    data=data,
    x='category',
    y='value',
    hue='group',
    showfliers=False,
    title='Transparent Boxes with Opaque Points',
    xlabel='Category',
    ylabel='Value',
    alpha=0.05,  # Very transparent boxes
)

# Overlay swarm plot with full opacity
pp.swarmplot(
    data=data,
    x='category',
    y='value',
    hue='group',
    dodge=True,
    ax=ax,
    alpha=1,
    size=4,
    legend=False
)
plt.show()

# %%
# Horizontal Combined Plot
# ------------------------
# Horizontal orientation works for both box and swarm plots.

# Create horizontal combined plot
fig, ax = pp.boxplot(
    data=data[data['group'] == 'Group 1'],
    x='value',
    y='category',
    showfliers=False,
    title='Horizontal Box + Swarm',
    xlabel='Value',
    ylabel='Category',
)

pp.swarmplot(
    data=data[data['group'] == 'Group 1'],
    x='value',
    y='category',
    ax=ax,
    alpha=1,
    size=4,
    legend=False
)
plt.show()
