# PubliPlots

Publication-ready plots

## Overview

PubliPlots is a Python visualization library that provides beautiful, publication-ready plots with a seaborn-like API. It focuses on:

- **Beautiful defaults**: Carefully designed pastel color palettes and styles
- **Intuitive API**: Follows seaborn conventions for ease of use
- **Modular design**: Compose complex visualizations from simple building blocks
- **Highly configurable**: Extensive customization while maintaining sensible defaults
- **Publication-ready**: Optimized for scientific publications and presentations

## Installation

### From PyPI

```bash
pip install publiplots
```

Or if you are using [uv](https://github.com/astral-sh/uv) for Python environment management:

```bash
uv pip install publiplots
```

### From source (development)

```bash
git clone https://github.com/jorgebotas/publiplots.git
cd publiplots
pip install -e .
```

### Development with uv and Jupyter

If you're using [uv](https://github.com/astral-sh/uv) for Python environment management and want to use the package in Jupyter notebooks:

```bash
# Clone the repository
git clone https://github.com/jorgebotas/publiplots.git
cd publiplots

# Create a new uv environment with Python 3.11 (or your preferred version)
uv venv --python 3.11

# Activate the environment
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate  # On Windows

# Install the package in editable mode with all dependencies
uv pip install -e .

# Install ipykernel to make the environment available in Jupyter
uv pip install ipykernel

# Register the environment as a Jupyter kernel
python -m ipykernel install --user --name=publiplots --display-name="Python (publiplots)"
```

Now you can select the "Python (publiplots)" kernel in Jupyter Lab or Jupyter Notebook and import publiplots:

```python
import publiplots as pp
```


## Quick Start

```python
import publiplots as pp
import pandas as pd

# Apply publication style globally
pp.set_publication_style()

# Create a scatter plot
fig, ax = pp.scatterplot(
    data=df,
    x='measurement_a',
    y='measurement_b',
    hue='condition',
    palette=pp.get_palette('pastel_categorical', n_colors=3)
)

# Save with publication-ready settings
pp.savefig(fig, 'figure.pdf')
```

## Features

### Base Plotting Functions

- `scatterplot()` - Scatter plots with flexible styling
- `barplot()` - Bar plots with error bars and grouping

### Advanced Functions

- `venn()` - 2-way and 3-way Venn diagrams

### Theming

- Pastel color palettes optimized for publications
- Customizable matplotlib styles
- Consistent styling across all plots

## Documentation

Full documentation is available at [github.com/jorgebotas/publiplots](https://github.com/jorgebotas/publiplots)

## Development Status

PubliPlots is currently in active development (v0.1.0). The API may change in future releases.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Citation

If you use PubliPlots in your research, please cite:

```
Botas, J. (2025). PubliPlots: Publication-ready plotting for Python.
GitHub: https://github.com/jorgebotas/publiplots
```

## License

MIT License - see LICENSE file for details.

## Author

Jorge Botas ([@jorgebotas](https://github.com/jorgebotas))

## Acknowledgments

PubliPlots builds upon excellent work from the Python visualization community:

- **[pyvenn](https://github.com/LankyCyril/pyvenn)** by LankyCyril - The Venn diagram implementation (2-6 sets) is adapted from this library
- **[matplotlib](https://matplotlib.org/)** - The foundational plotting library that powers PubliPlots
- **[seaborn](https://seaborn.pydata.org/)** - Inspiration for API design and color palettes
