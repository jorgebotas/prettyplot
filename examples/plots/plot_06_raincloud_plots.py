"""
Raincloud Plot Examples
=======================

This example demonstrates raincloud plot functionality in PubliPlots,
which combines violin plots (clouds), box plots (umbrellas), and strip/swarm plots (rain)
to show both distribution shapes and individual data points.

Examples
--------
"""

import publiplots as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set style
pp.set_notebook_style()

# %%
# Simple Raincloud Plot
# ~~~~~~~~~~~~~~~~~~~~~
# Basic raincloud plot showing distribution by category.

# Create sample data
np.random.seed(42)
n = 200
raincloud_data = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C', 'D'], n // 4),
    'value': np.concatenate([
        np.random.normal(10, 2, n // 4),
        np.random.normal(15, 3, n // 4),
        np.random.normal(12, 2.5, n // 4),
        np.random.normal(18, 4, n // 4)
    ])
})

# Create simple raincloud plot
fig, ax = pp.raincloudplot(
    data=raincloud_data,
    x='category',
    y='value',
    title='Simple Raincloud Plot',
    xlabel='Category',
    ylabel='Value',
    cloud_alpha=0.6,
)
plt.show()

# %%
# Raincloud Plot with Hue Grouping (Vertical)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Use the hue parameter to create grouped raincloud plots.

# Add group variable
raincloud_data['group'] = np.tile(['Group 1', 'Group 2'], n // 2)

# Create grouped raincloud plot
fig, ax = pp.raincloudplot(
    data=raincloud_data,
    x='category',
    y='value',
    hue='group',
    gap=0.1,
    title='Grouped Raincloud Plot',
    xlabel='Category',
    ylabel='Value',
    cloud_alpha=0.6,
    palette=['#5D83C3', '#e67e7e'],
)
plt.show()

# %%
# Horizontal Raincloud Plot with Hue
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create horizontal raincloud plots by swapping x and y.

fig, ax = pp.raincloudplot(
    data=raincloud_data,
    x='value',
    y='category',
    hue='group',
    gap=0.1,
    cloud_side='left',
    title='Horizontal Raincloud Plot',
    xlabel='Value',
    ylabel='Category',
    cloud_alpha=0.6,
    palette=['#5D83C3', '#e67e7e'],
    figsize=(4, 6),
)
plt.show()

# %%
# Customization
# -------------
#
# Raincloud Plot Without Box
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create raincloud plot with only cloud and rain elements.

fig, ax = pp.raincloudplot(
    data=raincloud_data[raincloud_data['group'] == 'Group 1'],
    x='category',
    y='value',
    box=False,
    title='Raincloud without Box Plot',
    xlabel='Category',
    ylabel='Value',
    cloud_alpha=0.6,
)
plt.show()

# %%
# Raincloud Plot with Custom Cloud Side
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Control which side the cloud appears on.

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Cloud on the left
pp.raincloudplot(
    data=raincloud_data[raincloud_data['group'] == 'Group 1'],
    x='category',
    y='value',
    cloud_side='left',
    ax=axes[0],
    title='Cloud on Left',
    xlabel='Category',
    ylabel='Value',
    cloud_alpha=0.6,
)

# Cloud on the right (default)
pp.raincloudplot(
    data=raincloud_data[raincloud_data['group'] == 'Group 1'],
    x='category',
    y='value',
    cloud_side='right',
    ax=axes[1],
    title='Cloud on Right',
    xlabel='Category',
    ylabel='Value',
    cloud_alpha=0.6,
)

plt.tight_layout()
plt.show()

# %%
# Raincloud Plot with Custom Alpha Values
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Adjust transparency of different components.

fig, ax = pp.raincloudplot(
    data=raincloud_data,
    x='category',
    y='value',
    hue='group',
    gap=0.1,
    title='Raincloud with Custom Alpha',
    xlabel='Category',
    ylabel='Value',
    cloud_alpha=0.3,
    box_alpha=0.5,
    rain_alpha=0.8,
    palette=['#5D83C3', '#e67e7e'],
)
plt.show()
