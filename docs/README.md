# PubliPlots Documentation

This directory contains the Sphinx documentation for PubliPlots, including:
- API reference documentation generated from docstrings
- Example gallery generated with sphinx-gallery
- User guides and tutorials

## Building the Documentation

### Prerequisites

Install the documentation dependencies:

```bash
pip install -e ".[docs]"
```

This will install:
- Sphinx and extensions
- sphinx-gallery for example gallery generation
- sphinx-rtd-theme for the Read the Docs theme
- numpydoc for NumPy-style docstring parsing
- pillow for image processing

### Build HTML Documentation

```bash
cd docs
make html
```

The built documentation will be in `build/html/`. Open `build/html/index.html` in a browser to view it.

### Clean Build

To remove all generated files and rebuild from scratch:

```bash
make clean-all
make html
```

This is useful when:
- You've made significant changes to the structure
- Examples aren't regenerating properly
- You want to ensure a clean build

### Other Build Formats

```bash
make latexpdf  # Build PDF documentation (requires LaTeX)
make epub      # Build EPUB format
make help      # See all available targets
```

## Documentation Structure

```
docs/
├── source/              # Source files for documentation
│   ├── conf.py         # Sphinx configuration
│   ├── index.rst       # Main documentation index
│   ├── api/            # API reference configuration
│   │   └── index.rst   # API documentation index
│   ├── _static/        # Static files (CSS, images)
│   └── _templates/     # Custom Sphinx templates
├── build/              # Generated documentation (gitignored)
│   └── html/          # HTML output
├── Makefile           # Build commands (Unix/Mac)
├── make.bat           # Build commands (Windows)
└── requirements.txt   # Documentation dependencies
```

## Example Gallery

The example gallery is automatically generated from Python scripts in the `examples/` directory (at the project root) using sphinx-gallery.

Each example:
- Is executed during the build process
- Generates an HTML page with code and output
- Creates a Jupyter notebook (.ipynb) for download
- Produces plots as images
- Is available as a downloadable Python script

To add a new example, create a Python file in `examples/` starting with `plot_` and following the sphinx-gallery format (see existing examples).

## API Documentation

API documentation is automatically generated from docstrings using:
- `sphinx.ext.autodoc` - Extract docstrings
- `sphinx.ext.autosummary` - Generate summary tables
- `numpydoc` - Parse NumPy/Google style docstrings
- `sphinx.ext.napoleon` - Support for NumPy and Google docstring formats

## Continuous Integration

The documentation can be built automatically on CI/CD platforms:

### GitHub Actions Example

```yaml
- name: Build documentation
  run: |
    pip install -e ".[docs]"
    cd docs
    make html
```

### Read the Docs

This project is configured for Read the Docs. The `docs/requirements.txt` file specifies all dependencies needed for RTD builds.

## Troubleshooting

### Examples fail to build

If examples fail during the build:
1. Check that all dependencies are installed
2. Run the example script directly to see the error: `python examples/plot_example.py`
3. Look at the full error in the terminal output

### Intersphinx warnings

Warnings about intersphinx inventories not being fetchable are usually harmless. They occur when Sphinx can't download external documentation for cross-referencing. The documentation will still build correctly.

### Missing images

If images aren't showing:
1. Make sure examples are being executed (check for .py.md5 files in `source/auto_examples/`)
2. Try a clean build: `make clean-all && make html`

### Module import errors

If Sphinx can't import the package:
1. Make sure PubliPlots is installed: `pip install -e .`
2. Check that Python can find the module: `python -c "import publiplots"`

## Contributing to Documentation

When adding new features:
1. Write comprehensive docstrings in NumPy/Google format
2. Add examples to the `examples/` directory if appropriate
3. Update relevant documentation pages
4. Build and review the documentation locally before submitting

## Additional Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [sphinx-gallery](https://sphinx-gallery.github.io/)
- [Read the Docs](https://docs.readthedocs.io/)
- [NumPy docstring guide](https://numpydoc.readthedocs.io/)
