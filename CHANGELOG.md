# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.1.0] - 2025-11-05

### Added
- Initial release
- Base plotting functions:
  - `barplot()` - Bar plots with error bars and grouping
  - `scatterplot()` - Scatter plots with flexible styling
- Advanced plotting functions:
  - `venn()` - 2-way and 3-way Venn diagrams
- Theme system:
  - Pastel color palettes optimized for publications
  - Publication, minimal, and poster style presets
  - Customizable marker and hatch patterns
- Utilities:
  - Legend builders with custom handlers
  - File I/O with `savefig()`
  - Axes manipulation utilities
- Comprehensive documentation and examples

[0.1.0]: https://github.com/jorgebotas/publiplots/releases/tag/v0.1.0


## [0.2.0] - 2025-11-06

### Added
- Venn diagram support for 2 to upto 5 sets!
- Thanks to yanlinlin82/ggvenn for their amazing work on Venn diagram geometry
- Removed matplolib-venn dependencies

[0.2.0]: https://github.com/jorgebotas/publiplots/releases/tag/v0.2.0



## [0.3.0] - 2025-11-17

### Added

- Dynamic Venn diagrams (not precomputed) based on **[ggvenn](https://github.com/yanlinlin82/ggvenn)** geometry

- UpSet plots based on **[UpSetPlot](https://github.com/jnothman/UpSetPlot)**
 

[0.3.0]: https://github.com/jorgebotas/publiplots/releases/tag/v0.3.0