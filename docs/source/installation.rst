Installation
============

Requirements
------------

PubliPlots requires Python 3.9 or later and the following packages:

* matplotlib >= 3.5.0
* seaborn >= 0.12.0
* numpy >= 1.21.0
* pandas >= 1.3.0

Installing from PyPI
--------------------

The easiest way to install PubliPlots is using pip:

.. code-block:: bash

   pip install publiplots

Installing from Source
----------------------

To install the latest development version from GitHub:

.. code-block:: bash

   git clone https://github.com/jorgebotas/publiplots.git
   cd publiplots
   pip install -e .

Development Installation
------------------------

If you want to contribute to PubliPlots, install the development dependencies:

.. code-block:: bash

   pip install -e ".[dev]"

This will install additional packages for testing and code quality:

* pytest
* pytest-cov
* black
* mypy
* ruff

Documentation Dependencies
--------------------------

To build the documentation locally:

.. code-block:: bash

   pip install -e ".[docs]"

This will install Sphinx, sphinx-gallery, and related documentation tools.

Verifying Installation
-----------------------

To verify that PubliPlots is installed correctly:

.. code-block:: python

   import publiplots as pp
   print(pp.__version__)

This should print the installed version number.
