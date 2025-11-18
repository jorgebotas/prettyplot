# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parents[2] / "src"))

import publiplots

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PubliPlots'
copyright = '2025, Jorge Botas'
author = 'Jorge Botas'
release = publiplots.__version__
version = publiplots.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_gallery.gen_gallery',
    'numpydoc',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'shibuya'
html_static_path = ['_static']
html_logo = None
html_favicon = None

html_theme_options = {
    'github_url': 'https://github.com/jorgebotas/publiplots',
    'nav_links': [
        {
            'title': 'Home',
            'url': 'index',
        },
        {
            'title': 'API Reference',
            'url': 'api/modules',
        },
        {
            'title': 'Examples',
            'url': 'auto_examples/index',
        },
    ],
}

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = False

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'seaborn': ('https://seaborn.pydata.org/', None),
}

# Sphinx-gallery configuration
# First, ensure fonts are registered for gallery plots
import publiplots  # This will register the custom fonts

sphinx_gallery_conf = {
    'examples_dirs': ['../../examples/01_basic', '../../examples/02_advanced', '../../examples/03_customization'],
    'gallery_dirs': ['auto_examples/01_basic', 'auto_examples/02_advanced', 'auto_examples/03_customization'],
    'filename_pattern': r'.*\.py$',
    'backreferences_dir': 'gen_modules/backreferences',
    'doc_module': ('publiplots',),
    'reference_url': {
        'publiplots': None,
    },
    'remove_config_comments': True,
    'plot_gallery': True,
    'download_all_examples': False,
    'min_reported_time': 0,
    'matplotlib_animations': True,
    'image_scrapers': ('matplotlib',),
    'default_thumb_file': None,
    'line_numbers': False,
    'nested_sections': True,
}

# NumPyDoc settings
numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = False
