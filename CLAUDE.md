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
│   ├── const.py        # Tax curves and social security data (⚠️ needs refactoring)
│   ├── taxes_income.py # Income tax calculations
│   ├── taxes_other.py  # Solidarity and church tax
│   └── social_security.py  # Social security calculations
├── test/               # Test suite (unittest)
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

#### 2. Tax Data (`const.py`)
**⚠️ HIGH PRIORITY REFACTORING NEEDED**

Contains four main data structures:
- `__tax_curve`: Progressive income tax brackets by year
- `__social_security_curve`: Social security limits and rates
- `__soli_curve`: Solidarity tax parameters
- `__correction_factor_pensions`: Pension deduction factors

**Current Issues**:
- Hardcoded Python dictionaries
- Difficult to maintain and audit
- No schema validation
- 2023-2025 data has incomplete `const` values (set to None)
- Cannot easily extend to new years

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
- **Formatter**: Black (line length: 127)
- **Linter**: Flake8
- **Type Hints**: Use type hints for all public functions
- **Docstrings**: NumPy-style docstrings with Parameters, Returns, Examples

### Testing
**Current**: unittest framework
**Recommended**: Migrate to pytest

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

### Immediate Tasks

#### 1. Fix ReadTheDocs Build Action (High Priority)
**Status**: ⚠️ Needs Investigation

**Issue**: ReadTheDocs build may be failing or not configured

**Investigation Steps**:
1. Check if `.readthedocs.yml` exists (currently missing)
2. Verify docs build locally: `cd docs && make html`
3. Check Sphinx configuration in `docs/conf.py`
4. Verify all dependencies in `docs/requirements.txt`

**Recommended Action**:
Create `.readthedocs.yml` in project root:
```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.12"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - requirements: docs/requirements.txt
    - method: pip
      path: .
```

#### 2. Add/Check Tax Codes for 2024-2027 (High Priority)
**Status**: ⚠️ Incomplete Data

**Current State**:
- ✅ 2018-2022: Complete with all constants
- ⚠️ 2023-2025: Steps and rates present, but `const` values are None
- ❌ 2026-2027: Not implemented

**Required Data Sources**:
- [BMF Tarifhistorie](https://www.bmf-steuerrechner.de/Tarifhistorie_Steuerrechner.pdf)
- [BMF Lohnsteuerrechner](https://www.bmf-steuerrechner.de/)
- [Social Security Rates](https://www.lohn-info.de/sozialversicherungsbeitraege2024.html)

**Tasks**:
1. Calculate and fill in missing `const` values for 2023-2025 tax curves
2. Verify social security rates for 2024-2025
3. Research and add preliminary data for 2026-2027 (if available)
4. Update `config.py` validation to support new years
5. Add tests for new years

**Tax Curve Constants Explanation**:
The `const` values are polynomial coefficients used in German tax calculation:
- Bracket 0: No constants (below basic allowance, 0% tax)
- Bracket 1: [a, b] for linear progression zone
- Bracket 2: [a, b, c] for first progression zone
- Bracket 3: [a, b] for top tax rate

#### 3. Refactor const.py to Structured Data (Medium Priority)
**Status**: 📋 Planned

**Problem**:
- Hard to update/maintain
- No schema validation
- Difficult to audit changes
- Can't easily extend to new years
- Python dictionaries are not ideal for data storage

**Recommendation**:
Move to structured data files with validation

**Proposed Structure**:
```
data/
├── tax_curves/
│   ├── 2018.json
│   ├── 2019.json
│   ├── ...
│   └── 2025.json
├── social_security/
│   ├── 2018.json
│   ├── ...
│   └── 2025.json
├── soli_curve.json
└── pension_factors.json
```

**Implementation Plan**:
1. Create JSON schema for validation (using jsonschema or pydantic)
2. Create data migration script to convert `const.py` to JSON files
3. Create data loader in `const.py` to read JSON files
4. Add validation layer to ensure data integrity
5. Create data update tooling (CLI or scripts)
6. Update documentation for data maintenance
7. Version control data separately with clear commit messages

**Benefits**:
- Easy to review changes in PRs (diff JSON files)
- Can add schema validation
- Non-developers can update tax data
- Easier to automate data updates
- Better separation of code and data

**Example Schema**:
```python
from pydantic import BaseModel, Field

class TaxBracket(BaseModel):
    step: float = Field(gt=0)
    rate: float = Field(ge=0, le=1)
    const: list[float] | None = None

class TaxCurve(BaseModel):
    year: int = Field(ge=2018, le=2030)
    brackets: dict[int, TaxBracket]
```

#### 4. Improve Error Handling (Medium Priority)
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

#### 5. Migrate to Pytest (Low Priority)
**Status**: 📋 Nice to Have

**Current**: Using unittest
**In dev-dependencies**: pytest is available

**Benefits of pytest**:
- Simpler, more Pythonic test syntax
- Better fixtures and parametrization
- More informative failure messages
- Active development and plugin ecosystem
- Already used in CI workflow

**Migration Example**:
```python
# Before (unittest)
class TestMain(unittest.TestCase):
    def test_for_valid_main(self):
        self.assertAlmostEqual(
            main.calc_netto(30000, config=self.default_config),
            20554.38,
            delta=1
        )

# After (pytest)
@pytest.mark.parametrize("salary,expected", [
    (30000, 20554.38),
    (60000, 35796.68),
    (90000, 49956.92),
    (120000, 64965.08),
])
def test_calc_netto(salary, expected, default_config):
    assert abs(main.calc_netto(salary, config=default_config) - expected) < 1
```

**Migration Steps**:
1. Convert one test file as proof of concept
2. Create pytest fixtures for common configs
3. Use parametrize for data-driven tests
4. Convert remaining test files
5. Remove unittest imports
6. Update documentation

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
# Run all tests with unittest
python -m unittest discover test/

# Run with pytest (preferred)
python -m pytest test/ -v

# Run with coverage
python -m pytest --cov=netto test/

# Run specific test file
python -m pytest test/test_main.py -v
```

### Building Documentation

```bash
cd docs/
make html
# Open docs/_build/html/index.html in browser
```

### Linting and Formatting

```bash
# Format with black
black netto/ test/ examples/

# Lint with flake8
flake8 netto/ test/ --max-line-length=127
```

### Local Development

```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -r requirements-dev.txt

# Run examples
python examples/examples.py
```

### Updating Tax Data

**Current Process** (needs improvement):
1. Edit `netto/const.py` directly
2. Find relevant data from official sources
3. Update dictionaries with new year data
4. Update validation in `config.py`
5. Add tests for new year
6. Verify calculations against official calculators

**Future Process** (after refactoring):
1. Create new JSON file in `data/tax_curves/YEAR.json`
2. Run validation script
3. Auto-update supported years list
4. Run tests against official calculators

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
- **Commit messages**: Conventional commits format
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for refactoring
  - `test:` for tests
  - `chore:` for maintenance

### CI/CD
- **Build Workflow** (`workflow.yml`): Runs on every push
  - Lint with flake8
  - Test on Python 3.10-3.14
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
| 2023 | ⚠️ Partial (const=None) | ✅ Complete | ✅ Complete | ⚠️ Needs completion |
| 2024 | ⚠️ Partial (const=None) | ✅ Complete | ✅ Complete | ⚠️ Needs completion |
| 2025 | ⚠️ Partial (const=None) | ✅ Complete | ✅ Complete | ⚠️ Needs completion |
| 2026 | ❌ Not started | ❌ NotImplementedError | ❌ Missing | ❌ Planned |
| 2027 | ❌ Not started | ❌ Missing | ❌ Missing | ❌ Planned |

---

**Last Updated**: 2024-11-14 (for release 0.2.0 preparation)
**Document Version**: 1.0
