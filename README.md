# PrettyPlot

Publication-ready plotting with a clean, modular API.

## Overview

PrettyPlot is a Python visualization library that provides beautiful, publication-ready plots with a seaborn-like API. It focuses on:

- **Beautiful defaults**: Carefully designed pastel color palettes and styles
- **Intuitive API**: Follows seaborn conventions for ease of use
- **Modular design**: Compose complex visualizations from simple building blocks
- **Highly configurable**: Extensive customization while maintaining sensible defaults
- **Publication-ready**: Optimized for scientific publications and presentations

## Installation

### From source (development)

#### Option 1: Using uv (recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver. If you don't have it installed:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then create a new environment and install prettyplot:

```bash
# Clone the repository
git clone https://github.com/jorgebotas/prettyplot.git
cd prettyplot

# Create a new virtual environment with uv
uv venv

# Activate the environment
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate   # On Windows

# Install the package in editable mode
uv pip install -e .
```

#### Option 2: Using pip

```bash
git clone https://github.com/jorgebotas/prettyplot.git
cd prettyplot
python -m venv venv
source venv/bin/activate  # On Linux/macOS
pip install -e .
```

### For Jupyter Notebook/Lab Integration

To use prettyplot in Jupyter notebooks, you need to install `ipykernel` and register the environment:

```bash
# Activate your environment first (if not already active)
source .venv/bin/activate  # or venv/bin/activate

# Install ipykernel and jupyter dependencies
uv pip install ipykernel jupyter
# or: pip install ipykernel jupyter

# Register the kernel with Jupyter
python -m ipykernel install --user --name=prettyplot --display-name="Python (prettyplot)"
```

Now you can select "Python (prettyplot)" as the kernel when creating or opening notebooks. Import prettyplot as usual:

```python
import prettyplot as pp
import pandas as pd
import numpy as np

# Your plotting code here
pp.set_publication_style()
```

### From PyPI (coming soon)

```bash
pip install prettyplot
```

## Quick Start

```python
import prettyplot as pp
import pandas as pd
import numpy as np

# Apply publication style globally
pp.set_publication_style()

# Example 1: Create a bar plot with grouped data
data = pd.DataFrame({
    'category': ['A', 'B', 'C', 'A', 'B', 'C'],
    'value': [10, 15, 13, 12, 18, 14],
    'group': ['Control', 'Control', 'Control', 'Treated', 'Treated', 'Treated']
})

fig, ax = pp.barplot(
    data=data,
    x='category',
    y='value',
    split='group',
    hue='category',
    palette=pp.get_palette('pastel_categorical', n_colors=3),
    hatch_mapping={'Control': '', 'Treated': '///'}
)

# Save with publication-ready settings
pp.savefig(fig, 'barplot.png', dpi=300)

# Example 2: Create a Venn diagram
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

fig, ax, stats = pp.venn_diagram(
    [set1, set2],
    labels=['Group A', 'Group B'],
    colors=pp.get_palette('pastel_categorical', n_colors=2)
)

pp.savefig(fig, 'venn.png', dpi=300)

# Example 3: Circle heatmap with size and color encoding
heatmap_data = pd.DataFrame({
    'x': ['Sample 1', 'Sample 2', 'Sample 1', 'Sample 2'],
    'y': ['Gene A', 'Gene A', 'Gene B', 'Gene B'],
    'size': [3.5, 2.1, 4.2, 1.8],
    'color': ['Up', 'Down', 'Up', 'Down']
})

fig, ax, cbar = pp.circle_heatmap(
    data=heatmap_data,
    x='x',
    y='y',
    size='size',
    hue='color',
    palette={'Up': '#75b375', 'Down': '#e67e7e'}
)

pp.savefig(fig, 'heatmap.png', dpi=300)
```

## Features

### Base Plotting Functions

- ✅ `barplot()` - Bar plots with error bars, grouping, and hatch patterns
- ✅ `circle_heatmap()` - Circle-based heatmaps with size and color encoding
- 🚧 `scatterplot()` - Scatter plots with flexible styling *(planned)*
- 🚧 `lineplot()` - Line plots with confidence intervals *(planned)*
- 🚧 `heatmap()` - Traditional heatmaps with annotations *(planned)*
- 🚧 `violinplot()` / `boxplot()` - Distribution visualizations *(planned)*

### Advanced Functions

- ✅ `venn_diagram()` - 2-way and 3-way Venn diagrams with statistical testing
- 🚧 `barplot_enrichment()` - Enrichment analysis with p-values *(planned)*
- 🚧 `barplot_overlap()` - Overlap analysis between groups *(planned)*

### Theming & Utilities

- ✅ **9 pastel color palettes** optimized for publications
  - Categorical, sequential, and diverging palettes
  - `get_palette()`, `list_palettes()`, `show_palette()`
- ✅ **Customizable matplotlib styles**
  - `set_publication_style()`, `set_minimal_style()`, `set_poster_style()`
- ✅ **Publication-ready I/O**
  - `savefig()` with 300 DPI defaults
  - `save_multiple()` for exporting to multiple formats
- ✅ **Axis manipulation utilities**
  - `adjust_spines()`, `add_grid()`, `add_reference_line()`, etc.
- ✅ **Input validation**
  - Comprehensive data validation and type checking

## Documentation

Full documentation is available at [github.com/jorgebotas/prettyplot](https://github.com/jorgebotas/prettyplot)

## Development Status

PrettyPlot is currently in active development (v0.1.0). The API may change in future releases.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Citation

If you use PrettyPlot in your research, please cite:

```
Botas, J. (2025). PrettyPlot: Publication-ready plotting for Python.
GitHub: https://github.com/jorgebotas/prettyplot
```

## License

MIT License - see LICENSE file for details.

## Author

Jorge Botas ([@jorgebotas](https://github.com/jorgebotas))
