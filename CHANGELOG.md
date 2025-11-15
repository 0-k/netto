# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-11-15

### Added
- **Data validation with Pydantic**: All tax and social security data now validated using Pydantic models
- **ReadTheDocs configuration**: Added `.readthedocs.yml` for proper documentation building
- **MANIFEST.in**: Ensures data files are included in package distribution
- **Comprehensive project documentation**: Added `CLAUDE.md` with detailed project guide for developers
- **Data directory structure**: Tax data now organized in JSON files for better maintainability:
  - `data/tax_curves/{year}.json` - Income tax brackets (2018-2025)
  - `data/social_security/{year}.json` - Social security rates (2018-2025)
  - `data/soli/{year}.json` - Solidarity tax parameters (2018-2025)
  - `data/pension_factors/{year}.json` - Pension correction factors (2018-2025)
  - `data/README.md` - Documentation for tax data structure and sources
- **Data loader module**: New `netto.data_loader` module with:
  - Pydantic models: `TaxCurve`, `SocialSecurity`, `SoliCurve`, `PensionFactor`
  - Validation functions for all data types
  - Module-level variables for easy import
- **Dependencies**: Added `pydantic>=2.0` for data validation

### Changed
- **BREAKING**: Refactored data storage from hardcoded Python dictionaries to validated JSON files
- **BREAKING**: Removed `netto.const` module - import from `netto.data_loader` instead
- **Version**: Updated from 0.1.x to 0.2.0
- **Copyright years**: Updated to 2025 in LICENSE, README.md, and documentation
- **Documentation version**: Updated Sphinx docs to version 0.2.0
- **Supported tax years**: Updated README to reflect 2018-2025 support
- **Package configuration**: Added explicit package discovery in `pyproject.toml`
- **Dependencies**: Now declared in `pyproject.toml` (scipy, pydantic>=2.0)
- **Documentation dependencies**: Updated `docs/requirements.txt` with missing packages

### Removed
- **BREAKING**: `netto/const.py` module (replaced by `netto/data_loader.py`)
- **TODO list**: Removed from README.md (moved to CLAUDE.md for internal tracking)

### Fixed
- **ReadTheDocs build**: Fixed setuptools package discovery error
- **Documentation builds**: Added missing Sphinx dependencies (sphinx>=5.0, sphinx-rtd-theme)
- **Variable shadowing**: Fixed `UnboundLocalError` in `taxes_income.py`
- **Import paths**: Updated all modules to import from `data_loader` instead of `const`

### Technical Improvements
- **Better maintainability**: Tax data in JSON files vs. hardcoded Python
- **Schema validation**: Pydantic ensures data integrity
- **Clearer git history**: Individual yearly files make changes easier to review
- **Easier auditing**: JSON files can be compared against official sources
- **Scalability**: Simple to add new tax years (just create new JSON files)
- **Separation of concerns**: Data separated from code

### Migration Guide for 0.2.0

If you were importing from `netto.const`:

```python
# OLD (0.1.x) - No longer works
from netto.const import __tax_curve, __social_security_curve

# NEW (0.2.0) - Import from data_loader
from netto.data_loader import tax_curve, social_security_curve
```

Public API (`calc_netto`, `calc_inverse_netto`, `TaxConfig`) remains unchanged.

## [0.1.0] - 2023-XX-XX

### Added
- Initial release
- Calculate net income from gross salary (`calc_netto`)
- Calculate required gross salary for desired net income (`calc_inverse_netto`)
- Support for married couples (doubles tax brackets)
- Support for children (affects nursing insurance)
- Optional church tax
- Public health and pension insurance
- West-German pension deduction
- Tax years 2018-2024 support

[Unreleased]: https://github.com/0-k/netto/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/0-k/netto/releases/tag/v0.2.0
[0.1.0]: https://github.com/0-k/netto/releases/tag/v0.1.0
