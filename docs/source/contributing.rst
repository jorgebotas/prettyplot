Contributing
============

We welcome contributions to PubliPlots! This document provides guidelines for contributing to the project.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/your-username/publiplots.git
      cd publiplots

3. Install development dependencies:

   .. code-block:: bash

      pip install -e ".[dev]"

Development Workflow
--------------------

1. Create a new branch for your feature or bugfix:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. Make your changes and add tests if applicable

3. Run the test suite:

   .. code-block:: bash

      pytest

4. Format your code:

   .. code-block:: bash

      black src/publiplots tests
      ruff check src/publiplots tests

5. Commit your changes with a clear commit message:

   .. code-block:: bash

      git commit -m "Add feature: description of your feature"

6. Push to your fork:

   .. code-block:: bash

      git push origin feature/your-feature-name

7. Create a pull request on GitHub

Code Style
----------

* Follow PEP 8 style guidelines
* Use Black for code formatting (line length: 88)
* Use type hints where appropriate
* Write clear, descriptive docstrings in NumPy/Google format

Testing
-------

* Add tests for new features in the ``tests/`` directory
* Ensure all tests pass before submitting a pull request
* Aim for high test coverage

Documentation
-------------

* Update documentation for any API changes
* Add examples for new features
* Use clear, concise language
* Follow the existing documentation style

Reporting Issues
----------------

When reporting issues, please include:

* A clear description of the problem
* Steps to reproduce the issue
* Expected vs. actual behavior
* Your environment (OS, Python version, PubliPlots version)
* Minimal code example demonstrating the issue

Feature Requests
----------------

We welcome feature requests! Please:

* Check if the feature already exists or has been requested
* Provide a clear use case for the feature
* Describe the proposed API or interface
* Be open to discussion and feedback

Code of Conduct
---------------

* Be respectful and inclusive
* Provide constructive feedback
* Focus on the issue, not the person
* Be patient with new contributors

Questions?
----------

If you have questions about contributing, please:

* Check the existing documentation
* Search for similar issues on GitHub
* Open a new issue with the "question" label

Thank you for contributing to PubliPlots!
