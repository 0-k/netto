# Claude.md - Netto Project Guide

## Project Overview

**Netto** is a German income tax (Einkommensteuer) and social security (Sozialabgaben) calculator written in Python. It calculates net income from gross salary considering various tax brackets, social security contributions, solidarity tax (Solidaritätszuschlag), and optional church tax.

**Current Version**: 0.2.0 (in preparation)

**Supported Tax Years**: 2018-2025 (with plans to extend to 2026-2027)

**Key Features**:
- Calculate net income from gross salary (`calc_netto`)
- Calculate required gross salary for desired net income (`calc_inverse_netto`)
- Support for married couples (doubles tax brackets)
- Support for children (affects nursing insurance)
- Optional church tax
- Public health and pension insurance
- West-German pension deduction

## Architecture

### Project Structure

```
netto/
├── netto/               # Main library code
│   ├── __init__.py     # Package initialization
│   ├── main.py         # Main API (calc_netto, calc_inverse_netto)
│   ├── config.py       # TaxConfig dataclass
│   ├── data_loader.py  # Data loader with Pydantic validation
│   ├── taxes_income.py # Income tax calculations
│   ├── taxes_other.py  # Solidarity and church tax
│   └── social_security.py  # Social security calculations
├── data/               # Tax data (JSON files with validation)
│   ├── tax_curves/     # Income tax brackets by year
│   ├── social_security/ # Social security rates by year
│   ├── soli/           # Solidarity tax parameters
│   ├── pension_factors/ # Pension correction factors
│   └── README.md       # Data structure documentation
├── test/               # Test suite (pytest)
├── docs/               # Sphinx documentation
├── examples/           # Usage examples
└── .github/workflows/  # CI/CD pipelines
```

### Core Components

#### 1. Configuration (`config.py`)
- **TaxConfig dataclass**: Central configuration for all calculations
  - `year`: Tax year (2018-2025)
  - `has_children`: Affects nursing insurance extra rate
  - `is_married`: Doubles tax brackets (Ehegattensplitting)
  - `extra_health_insurance`: Additional health insurance rate (default: 0.014)
  - `church_tax`: Church tax rate (default: 0.09, set to 0.0 for none)
- Includes validation in `__post_init__`

#### 2. Tax Data (`data_loader.py`)
**✅ REFACTORED TO STRUCTURED DATA**

Contains data loader with Pydantic validation for:
- `tax_curve`: Progressive income tax brackets by year
- `social_security_curve`: Social security limits and rates
- `soli_curve`: Solidarity tax parameters
- `pension_factors`: Pension deduction factors

**Benefits of Current Structure**:
- JSON files in `data/` directory for easy editing
- Pydantic schema validation ensures data integrity
- Easy to audit changes via git diffs
- Simple to extend to new years (just add new JSON files)
- Clear separation between code and data

#### 3. Main API (`main.py`)

**calc_netto(salary, deductibles=0, verbose=False, config=None)**
- Calculates net income from gross salary
- Returns rounded float (2 decimal places)
- Workflow:
  1. Calculate deductible social security (`calc_deductible_social_security`)
  2. Calculate taxable income (`calc_taxable_income`)
  3. Calculate income tax via integration (`calc_income_tax_by_integration`)
  4. Calculate soli, church tax, social security
  5. Return: salary - all taxes and contributions

**calc_inverse_netto(desired_netto, deductibles=0, config=None)**
- Calculates required gross salary for desired net income
- Uses Newton's method for optimization (scipy.optimize.newton)
- Returns rounded integer

#### 4. Tax Calculations

**Income Tax** (`taxes_income.py`):
- Progressive tax curve with 4 brackets (0-3)
- German tax formula implementation
- Integration-based calculation for accuracy

**Other Taxes** (`taxes_other.py`):
- **Solidarity Tax (Soli)**: Reduced significantly in 2021
  - Pre-2021: 5.5% on income tax above threshold
  - 2021+: Phased reduction, only affects high earners
- **Church Tax**: Optional, typically 8-9% of income tax

**Social Security** (`social_security.py`):
- Pension insurance (Rentenversicherung)
- Unemployment insurance (Arbeitslosenversicherung)
- Health insurance (Krankenversicherung)
- Nursing care insurance (Pflegeversicherung)
  - Extra rate for childless individuals (Kinderlosenzuschlag)

## Development Guidelines

### Code Style
- **Formatter & Linter**: Ruff (line length: 88)
  - Replaces Black, isort, and Flake8 with a single fast tool
  - Uses Black-compatible 88 character line length (industry standard)
  - Configuration in `pyproject.toml`
- **Type Hints**: Use type hints for all public functions
- **Docstrings**: NumPy-style docstrings with Parameters, Returns, Examples

### Testing
**Framework**: pytest (migrated from unittest)

**Test Coverage**:
- Target: >80% code coverage
- CI runs pytest with coverage reporting to Codecov
- Tests should cover:
  - Various salary ranges
  - Different configurations (married, children, church tax)
  - Edge cases (zero income, very high income)
  - Inverse calculations

### Python Version Support
- **Minimum**: Python 3.10
- **Tested**: 3.10, 3.11, 3.12, 3.13, 3.14
- Uses modern Python features (dataclasses with slots, union types with `|`)

## Release 0.2.0 - Preparation Tasks

### Remaining Tasks

#### 1. Add/Check Tax Codes for 2024-2027 (High Priority)
**Status**: ⚠️ Incomplete Data

**Current State**:
- ✅ 2018-2025: Complete with all constants
- ❌ 2026-2027: Not implemented

**Required Data Sources**:
- [BMF Tarifhistorie](https://www.bmf-steuerrechner.de/Tarifhistorie_Steuerrechner.pdf)
- [BMF Lohnsteuerrechner](https://www.bmf-steuerrechner.de/)
- [Social Security Rates](https://www.lohn-info.de/sozialversicherungsbeitraege2024.html)

**Tasks**:
1. Research and add preliminary data for 2026-2027 (if available from official sources)
2. Create JSON files in `data/` directory for 2026-2027
3. Update `config.py` validation to support new years
4. Add tests for new years
5. Verify calculations against official BMF calculators

**Tax Curve Constants Explanation**:
The `const` values are polynomial coefficients used in German tax calculation:
- Bracket 0: No constants (below basic allowance, 0% tax)
- Bracket 1: [a, b] for linear progression zone
- Bracket 2: [a, b, c] for first progression zone
- Bracket 3: [a, b] for top tax rate

#### 2. Improve Error Handling (Medium Priority)
**Status**: 📋 Planned

**Current Issues**:
- Limited input validation
- Generic error messages
- No custom exception types

**Recommendation**:

**A. Custom Exception Hierarchy**:
```python
# In netto/exceptions.py
class NettoError(Exception):
    """Base exception for netto library"""
    pass

class UnsupportedTaxYear(NettoError):
    """Tax year not supported"""
    pass

class InvalidSalary(NettoError):
    """Invalid salary value"""
    pass

class InvalidConfiguration(NettoError):
    """Invalid configuration"""
    pass
```

**B. Enhanced Validation**:
```python
def calc_netto(salary: float, ...) -> float:
    if salary < 0:
        raise InvalidSalary(f"Salary must be non-negative, got {salary}")

    if config.year not in SUPPORTED_YEARS:
        raise UnsupportedTaxYear(
            f"Year {config.year} not supported. "
            f"Supported years: {SUPPORTED_YEARS}"
        )

    if deductibles < 0:
        raise ValueError(f"Deductibles must be non-negative, got {deductibles}")
```

**C. Validation in TaxConfig**:
- Already has good validation in `__post_init__`
- Consider more specific exception types
- Add helpful error messages with valid ranges

### Completed Tasks

The following tasks have been completed in v0.2.0:

- ✅ **ReadTheDocs Configuration**: Added `.readthedocs.yml` for proper documentation building
- ✅ **Refactor const.py to Structured Data**: Migrated from hardcoded Python dictionaries to validated JSON files
- ✅ **Migrate to Pytest**: Converted test suite from unittest to pytest
- ✅ **Switch to Ruff**: Replaced Black, isort, and Flake8 with Ruff for faster linting and formatting

### Future Enhancements (Post 0.2.0)

From README TODO list:
- [ ] Calculate support for children (Kindergeld/Kinderfreibetrag)
- [ ] Implement correct pension deductible for East Germany
- [ ] Add support for self-employed individuals
- [ ] Add support for capital gains tax (Kapitalertragsteuer)
- [ ] Multi-year tax planning calculations

## Common Tasks

### Running Tests

```bash
# First, install package in editable mode (required for imports to work)
pip install -e .

# Run with pytest (use python -m to ensure correct environment)
python -m pytest test/ -v

# Run with coverage
python -m pytest --cov=netto test/

# Run specific test file
python -m pytest test/test_main.py -v

# Alternative: Use pytest's import mode (like CI does)
python -m pytest --import-mode=append test/
```

**Important**: Always use `python -m pytest` (not just `pytest`) to ensure tests run in the same Python environment where you installed the package. This avoids `ModuleNotFoundError` when using UV or other tool managers.

### Building Documentation

```bash
cd docs/
make html
# Open docs/_build/html/index.html in browser
```

### Linting and Formatting

```bash
# Format with ruff
ruff format .

# Lint with ruff
ruff check .

# Fix linting issues automatically
ruff check --fix .
```

### Local Development

```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks (recommended)
pre-commit install

# Run pre-commit on all files (optional, to test)
pre-commit run --all-files

# Run examples
python examples/examples.py
```

**Pre-commit hooks** automatically run ruff linting and formatting before each commit, preventing CI failures. This is highly recommended for all contributors.

### Updating Tax Data

**Current Process**:
1. Create new JSON file in `data/tax_curves/YEAR.json` (copy and modify from previous year)
2. Create new JSON file in `data/social_security/YEAR.json`
3. Create new JSON file in `data/soli/YEAR.json`
4. Create new JSON file in `data/pension_factors/YEAR.json`
5. Find relevant data from official sources (BMF, lohn-info.de)
6. Update JSON files with new year data
7. Update validation in `config.py` to support the new year
8. Add tests for new year
9. Verify calculations against official BMF calculators

**Data Validation**:
- All data is validated using Pydantic models in `data_loader.py`
- Invalid data will raise validation errors on import
- See `data/README.md` for detailed data structure documentation

### Release Process

See `RELEASE.md` for detailed instructions.

**Quick Checklist**:
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run tests locally
4. Build and verify: `python -m build && twine check dist/*`
5. Commit and push
6. Test on TestPyPI (via GitHub Actions)
7. Create GitHub release with tag `vX.Y.Z`
8. Automatic PyPI publish via trusted publishing

## Data Sources & References

### Official Sources
- **Tax Calculation Formulas**: [BMF Tarifhistorie](https://www.bmf-steuerrechner.de/Tarifhistorie_Steuerrechner.pdf)
- **Wage Tax Calculator**: [BMF Lohnsteuerrechner](https://www.bmf-steuerrechner.de/)
- **Social Security Deductible**: [Vorsorgepauschale](https://www.lohn-info.de/vorsorgepauschale.html)
- **Social Security Rates**: [Sozialversicherungsbeiträge](https://www.lohn-info.de/sozialversicherungsbeitraege2024.html)
- **Solidarity Tax**: [Solidaritätszuschlag](https://www.lohn-info.de/solizuschlag.html)

### Verification Tools
- [Taxable Income Calculator](https://udo-brechtel.de/mathe/est_gsv/reverse_zve_brutto.htm)
- BMF official calculators (various years)

### Important Tax Law Changes

**2021**: Major solidarity tax (Soli) reduction
- Changed from flat 5.5% to progressive phase-out
- Only affects high earners (>~60k single, >~120k married)
- Parameters: `start_taxable_income: 16956`, `start_fraction: 0.119`

**2022**: Nursing insurance extra rate increase
- Childless extra rate increased from 0.25% to 0.35%

**2023-2025**: Progressive basic allowance increases
- 2023: 10,909€
- 2024: 11,605€
- 2025: 12,086€

## Code Quality Standards

### Test Requirements
- All public functions must have tests
- Critical calculations should have verification tests against official calculators
- Edge cases must be covered (0, negative, very large values)
- Configuration combinations should be tested

### Documentation Requirements
- All public functions must have NumPy-style docstrings
- Include Examples section in docstrings
- Keep README.md up to date with supported years
- Update CHANGELOG.md for all releases

### Git Workflow
- **Main branch**: `master` (protected)
- **Feature branches**: `claude/feature-name-SESSION_ID`
- **Pre-commit hooks**: HIGHLY RECOMMENDED - install with `pre-commit install`
  - Automatically runs ruff linting and formatting before each commit
  - Prevents CI failures by catching issues locally
  - Ensures consistent code quality across all commits
- **Commit messages**: Conventional commits format
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for refactoring
  - `test:` for tests
  - `chore:` for maintenance
  - `style:` for code formatting/style changes

### CI/CD
- **Build Workflow** (`workflow.yml`): Runs on every push
  - Lint with ruff (`ruff check .`)
  - Format check with ruff (`ruff format --check .`)
  - Test on Python 3.10-3.14 with pytest
  - Upload coverage to Codecov
- **PyPI Publishing**:
  - TestPyPI: Manual trigger via GitHub Actions
  - PyPI: Automatic on GitHub release
  - Uses trusted publishing (OIDC, no API tokens)

## Troubleshooting

### Common Issues

**Issue**: Tests fail with import errors
**Solution**: Install package in development mode: `pip install -e .`

**Issue**: Tax calculations don't match official calculators
**Solution**:
1. Verify correct year is set in config
2. Check that all parameters match (married, church tax, etc.)
3. Verify const values for that year are complete
4. Check for rounding differences (netto rounds to 2 decimals)

**Issue**: Type errors with Python 3.10
**Solution**: Ensure using `from __future__ import annotations` or use `Union[X, Y]` instead of `X | Y`

**Issue**: ReadTheDocs build fails
**Solution**:
1. Create `.readthedocs.yml` (see above)
2. Verify `docs/requirements.txt` has all Sphinx dependencies
3. Test locally: `cd docs && make html`

## Contact & Credits

**Author**: Martin Klein (hi@martinklein.co)
**Repository**: https://github.com/0-k/netto
**Documentation**: https://netto.readthedocs.io/
**License**: MIT

## Quick Reference

### Key Functions
```python
from netto import calc_netto, calc_inverse_netto
from netto.config import TaxConfig

# Basic usage
net = calc_netto(50000)  # Uses defaults (2022, single, no church tax)

# Custom configuration
config = TaxConfig(year=2024, is_married=True, has_children=True, church_tax=0.0)
net = calc_netto(50000, config=config)

# Inverse calculation
gross = calc_inverse_netto(35000, config=config)

# With deductibles and verbose output
net = calc_netto(50000, deductibles=2000, verbose=True, config=config)
```

### Tax Year Support Matrix

| Year | Tax Curve | Social Security | Soli | Status |
|------|-----------|-----------------|------|--------|
| 2018 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Fully supported |
| 2019 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Fully supported |
| 2020 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Fully supported |
| 2021 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Fully supported |
| 2022 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Fully supported |
| 2023 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Fully supported |
| 2024 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Fully supported |
| 2025 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Fully supported |
| 2026 | ❌ Not started | ❌ Not started | ❌ Not started | ❌ Planned |
| 2027 | ❌ Not started | ❌ Not started | ❌ Not started | ❌ Planned |

---

**Last Updated**: 2025-11-15 (for release 0.2.0a3)
**Document Version**: 1.1
