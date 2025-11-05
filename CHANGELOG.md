# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Renamed package from `prettyplot` to `prettyplots` to avoid PyPI name conflict

## [0.1.0] - 2025-01-XX

### Added
- Initial release
- Base plotting functions:
  - `barplot()` - Bar plots with error bars and grouping
  - `scatterplot()` - Scatter plots with flexible styling
  - `circle_heatmap()` - Circle-based heatmaps with size encoding
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

[Unreleased]: https://github.com/jorgebotas/prettyplots/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jorgebotas/prettyplots/releases/tag/v0.1.0
