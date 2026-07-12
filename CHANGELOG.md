# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-12

### Added
- **Dual-income households**: New `partner_salary` parameter on `calc_netto` and
  `calc_inverse_netto` for jointly assessed couples where both partners work
  - Income tax is assessed jointly (Ehegattensplitting) on the combined income
  - Social security contributions are calculated per person against the
    individual contribution ceilings (Beitragsbemessungsgrenzen)
  - Each earner receives their own Werbungskosten-Pauschbetrag
  - `calc_inverse_netto` solves for the primary salary with the partner salary fixed
- **Lump-sum deductions data**: New `data/deductions/{year}.json` files with
  year-specific Werbungskosten-Pauschbetrag (1,000 € until 2021, 1,200 € in 2022,
  1,230 € since 2023) and Sonderausgaben-Pauschbetrag, validated via the new
  `Deductions` Pydantic model
- **Tax year 2026 support**: Added preliminary tax data for 2026
  - Income tax brackets with estimated values
  - Social security rates and contribution limits
  - Solidarity tax parameters
  - Pension correction factors
- **Pre-commit hooks**: Added `.pre-commit-config.yaml` for automatic code quality checks
  - Runs ruff linting with auto-fix before each commit
  - Runs ruff formatting before each commit
  - Prevents CI failures by catching issues locally
  - Added `pre-commit` to development dependencies
- **TaxConfig dataclass**: New `TaxConfig` dataclass for explicit, type-safe configuration
  - Replaces environment variable-based configuration
  - Provides validation in `__post_init__`
  - Supports year (2018-2026), has_children, is_married, extra_health_insurance, church_tax
- **Data validation with Pydantic**: All tax and social security data now validated using Pydantic models
- **ReadTheDocs configuration**: Added `.readthedocs.yml` for proper documentation building
- **MANIFEST.in**: Ensures data files are included in package distribution
- **Comprehensive project documentation**: Added `CLAUDE.md` with detailed project guide for developers
- **Data directory structure**: Tax data now organized in JSON files for better maintainability:
  - `data/tax_curves/{year}.json` - Income tax brackets (2018-2026)
  - `data/social_security/{year}.json` - Social security rates (2018-2026)
  - `data/soli/{year}.json` - Solidarity tax parameters (2018-2026)
  - `data/pension_factors/{year}.json` - Pension correction factors (2018-2026)
  - `data/README.md` - Documentation for tax data structure and sources
- **Data loader module**: New `netto.data_loader` module with:
  - Pydantic models: `TaxCurve`, `SocialSecurity`, `SoliCurve`, `PensionFactor`
  - Validation functions for all data types
  - Module-level variables for easy import
- **Dependencies**: Added `pydantic>=2.0` for data validation
- **Type hints**: Added throughout the codebase for better IDE support
- **Explicit public API**: Defined `__all__` in `__init__.py`

### Changed
- **Code Quality Tools**: Migrated from Black, isort, and Flake8 to Ruff
  - Single, faster tool for formatting and linting
  - Configuration in `pyproject.toml`
  - Line length set to 88 (Black-compatible, industry standard)
  - Updated CI workflow to use Ruff
  - Updated development dependencies in `requirements-dev.txt`
  - Applied ruff formatting and linting fixes across entire codebase
- **README.md**: Completely redesigned for better usability
  - Added comprehensive feature list
  - Added installation instructions
  - Added quick start examples (basic, custom config, with deductibles)
  - Added configuration reference table
  - Added development setup instructions
  - Added code quality commands using Ruff
  - Updated badge from "Code style: black" to Ruff badge
- **CLAUDE.md**: Updated project documentation
  - Updated project structure to reflect `data/` directory instead of `const.py`
  - Updated Code Style section to mention Ruff instead of Black/Flake8
  - Updated Testing section to reflect pytest migration (completed)
  - Updated Linting and Formatting section with Ruff commands
  - Updated Updating Tax Data section to reflect new JSON-based workflow
  - Updated CI/CD section to mention Ruff
  - Moved completed tasks to "Completed Tasks" section
  - Updated Tax Year Support Matrix (2018-2026 now fully supported)
- **BREAKING**: Configuration system completely refactored:
  - Environment variable support removed (`NETTO_YEAR`, etc. no longer work)
  - All functions now accept optional `config: TaxConfig` parameter
  - Defaults to `TaxConfig()` with sensible defaults (year=2025, single, no church tax)
  - No more global state or hidden configuration
- **BREAKING**: Refactored data storage from hardcoded Python dictionaries to validated JSON files
- **BREAKING**: Removed `netto.const` module - import from `netto.data_loader` instead
- **BREAKING**: Python 3.10+ required (was 3.8+)
- **Version**: Updated from 0.1.x to 0.2.0
- **Copyright years**: Updated to 2025 in LICENSE, README.md, and documentation
- **Documentation version**: Updated Sphinx docs to version 0.2.0
- **Supported tax years**: Updated README to reflect 2018-2026 support
- **Package configuration**: Added explicit package discovery in `pyproject.toml`
- **Dependencies**: Now declared in `pyproject.toml` (scipy, pydantic>=2.0)
- **Documentation dependencies**: Updated `docs/requirements.txt` with missing packages
- **Default year**: Updated default year from 2022 to 2025
- **Health insurance rate**: Updated default extra health insurance rate from 1.4% to 2.5%

### Removed
- **Development Dependencies**: Removed Black, isort, and Twine from `requirements-dev.txt`
  - Replaced with Ruff for formatting and linting
  - Twine removed as it's not needed for modern PyPI publishing workflow
- **BREAKING**: Environment variable configuration support (no more `NETTO_YEAR`, `NETTO_MARRIED`, etc.)
- **BREAKING**: `load_config_from_env()` function removed
- **BREAKING**: `get_default_config()` function removed
- **BREAKING**: Global configuration state removed
- **BREAKING**: `netto/const.py` module (replaced by `netto/data_loader.py`)
- **TODO list**: Removed from README.md (moved to CLAUDE.md for internal tracking)

### Fixed
- **Solidarity tax for married couples**: The soli exemption threshold (Freigrenze)
  is now doubled for jointly assessed couples. Previously, married couples were
  charged up to ~2,200 €/year too much soli in the mid-to-high income range
- **Year-specific lump-sum deductions**: `calc_taxable_income` no longer hardcodes
  the 2022 Werbungskosten-Pauschbetrag (1,200 €) for all years, and the
  Sonderausgaben-Pauschbetrag is doubled for married couples (72 € instead of 36 €)
- **Married income tax via exact formula**: `calc_income_tax` now applies the
  splitting tariff (2 × tax(income/2)) for married couples, consistent with
  `calc_income_tax_by_integration`
- **Test rounding tolerance**: Adjusted test assertions to use appropriate rounding tolerance for floating-point comparisons
- **Tax curve polynomial coefficients**: Added missing coefficients and corrected bracket boundaries for 2021-2025
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

**1. Configuration Changes:**

```python
# OLD (0.1.x) - Environment variables
import os
os.environ['NETTO_YEAR'] = '2024'
os.environ['NETTO_MARRIED'] = '1'
from netto import calc_netto
calc_netto(50000)  # Used env vars

# NEW (0.2.0) - Explicit TaxConfig
from netto import calc_netto, TaxConfig

# Use defaults
calc_netto(50000)  # year=2022, single, no church tax

# Or explicit config
config = TaxConfig(year=2024, is_married=True)
calc_netto(50000, config=config)
```

**2. Internal imports (if you were using them):**

```python
# OLD (0.1.x) - No longer works
from netto.const import __tax_curve, __social_security_curve

# NEW (0.2.0) - Import from data_loader
from netto.data_loader import tax_curve, social_security_curve
```

**3. Python version requirement:**
- Minimum Python version is now 3.10 (was 3.8)

## [0.1.0] - 2023-05-19

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
