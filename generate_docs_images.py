
import publiplots as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory
os.makedirs('docs/images', exist_ok=True)

# Set style
pp.set_publication_style()

# 1. Barplot with hatch+hue
print("Generating barplot with hatch+hue...")
np.random.seed(666)
treatment_data = pd.DataFrame({
    'tissue': np.repeat(['Liver', 'Kidney', 'Heart'], 15),
    'treatment': np.tile(['Control']*7 + ['Treatment']*8, 3),
    'response': np.concatenate([
        # Liver
        np.random.normal(85, 8, 7),    # Control
        np.random.normal(110, 12, 8),  # Treatment
        # Kidney
        np.random.normal(90, 9, 7),    # Control
        np.random.normal(115, 13, 8),  # Treatment
        # Heart
        np.random.normal(80, 7, 7),    # Control
        np.random.normal(105, 11, 8),  # Treatment
    ])
})

pp.set_hatch_mode(3)
fig, ax = pp.barplot(
    data=treatment_data,
    x='tissue',
    y='response',
    hue='treatment',
    hatch='treatment',
    title='Tissue Response: Color + Hatch Patterns',
    xlabel='Tissue Type',
    ylabel='Response Level',
    errorbar='se',
    palette={'Control': '#8E8EC1', 'Treatment': '#75B375'},
    hatch_map={'Control': '', 'Treatment': '//'},
    alpha=0.3,
)
pp.savefig('docs/images/barplot_hatch_hue.png', dpi=300)
plt.close(fig)
pp.set_hatch_mode()

# 2. Raincloud plot with hues
print("Generating raincloud plot with hues...")
np.random.seed(123)
grouped_raincloud_data = pd.DataFrame({
    'time': np.repeat(['Day 1', 'Day 3', 'Day 7'], 40),
    'group': np.tile(np.repeat(['Control', 'Treated'], 20), 3),
    'measurement': np.concatenate([
        np.random.normal(50, 8, 20), np.random.normal(52, 8, 20),
        np.random.normal(52, 9, 20), np.random.normal(70, 12, 20),
        np.random.normal(55, 10, 20), np.random.normal(85, 14, 20),
    ])
})
grouped_raincloud_data = grouped_raincloud_data[grouped_raincloud_data['time'].isin(['Day 1', 'Day 3'])]
fig, ax = pp.raincloudplot(
    data=grouped_raincloud_data,
    x='time',
    y='measurement',
    hue='group',
    gap=0.1,
    title='Horizontal Raincloud: Control vs Treated',
    xlabel='Measurement',
    ylabel='Time Point',
    cloud_alpha=0.6,
    palette={'Control': '#5D83C3', 'Treated': '#e67e7e'},
    cloud_side="left",
)
pp.savefig('docs/images/raincloud_hue.png', dpi=300)
plt.close(fig)

# 3. 4-way Venn diagram
print("Generating 4-way Venn diagram...")
np.random.seed(888)
set1 = set(np.random.randint(1, 120, 70))
set2 = set(np.random.randint(30, 150, 75))
set3 = set(np.random.randint(60, 180, 70))
set4 = set(np.random.randint(1, 100, 65))

fig, ax = pp.venn(
    sets=[set1, set2, set3, set4],
    labels=['Dataset A', 'Dataset B', 'Dataset C', 'Dataset D'],
    colors=pp.color_palette('pastel', n_colors=4),
    figsize=(6, 6),
)
pp.savefig('docs/images/venn_4way.png', dpi=300)
plt.close(fig)

# 4. Upsetplot
print("Generating Upsetplot...")
np.random.seed(100)
upset_sets = {
    'Gene Set A': set(np.random.randint(1, 100, 50)),
    'Gene Set B': set(np.random.randint(30, 130, 55)),
    'Gene Set C': set(np.random.randint(60, 140, 45)),
    'Gene Set D': set(np.random.randint(20, 110, 48))
}

fig, axes = pp.upsetplot(
    data=upset_sets,
    sort_by='size',
    title='Customized UpSet Plot',
    color='#E67E7E',
    alpha=0.3,
    bar_linewidth=1.5,
    show_counts=12,
)
# Upsetplot returns a figure and axes, but savefig expects figure
pp.savefig('docs/images/upsetplot.png', dpi=300)
plt.close(fig)

print("All images generated successfully!")
