# netto

[![Documentation Status](https://readthedocs.org/projects/netto/badge/?version=latest)](https://netto.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/netto.svg)](https://pypi.python.org/pypi/netto)
[![CI](https://github.com/0-k/netto/actions/workflows/workflow.yml/badge.svg)](https://github.com/0-k/netto/actions/workflows/workflow.yml)
[![codecov](https://codecov.io/gh/0-k/netto/branch/master/graph/badge.svg)](https://codecov.io/gh/0-k/netto)
[![License](https://img.shields.io/pypi/l/netto.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**netto** is a German income tax (Einkommensteuer) and social security (Sozialabgaben) calculator written in Python. It calculates net income from gross salary considering various tax brackets, social security contributions, solidarity tax (Solidaritätszuschlag), and optional church tax.

## Features

- 💶 **Calculate net income** from gross salary with `calc_netto()`
- 💵 **Calculate required gross salary** for desired net income with `calc_inverse_netto()`
- 📅 **Support for tax years 2018-2025**
- 👨‍👩‍👧‍👦 **Married couples support** (Ehegattensplitting - doubles tax brackets)
- 👶 **Children support** (affects nursing care insurance extra rate)
- ⛪ **Optional church tax** (8-9%, configurable)
- 🏥 **Public health and pension insurance** calculations
- 📊 **West-German pension deduction** (East German support planned)
- ✅ **Type-safe configuration** with Pydantic validation
- 📚 **Comprehensive documentation** on [ReadTheDocs](https://netto.readthedocs.io/)

## Installation

Install from PyPI using pip:

```bash
pip install netto
```

Requires Python 3.10 or higher.

## Quick Start

### Basic Usage

```python
from netto import calc_netto

# Calculate net income from 50,000€ gross salary (uses defaults)
net_income = calc_netto(50000)
print(f"Net income: {net_income}€")
# Output: Net income: 30679.18€
```

### Custom Configuration

```python
from netto import calc_netto, calc_inverse_netto, TaxConfig

# Configure for 2024, married couple, with children, no church tax
config = TaxConfig(
    year=2024,
    is_married=True,
    has_children=True,
    church_tax=0.0,  # Set to 0.09 for 9% church tax
    extra_health_insurance=0.014  # Additional health insurance rate
)

# Calculate net income
net = calc_netto(50000, config=config)
print(f"Net income: {net}€")

# Calculate required gross salary for desired net income
gross = calc_inverse_netto(35000, config=config)
print(f"Required gross: {gross}€")
```

### With Deductibles and Verbose Output

```python
from netto import calc_netto, TaxConfig

config = TaxConfig(year=2024)

# Calculate with 2000€ deductibles and verbose output
net = calc_netto(
    salary=60000,
    deductibles=2000,  # e.g., professional expenses
    verbose=True,      # Print detailed breakdown
    config=config
)
```

## Configuration

The `TaxConfig` dataclass provides type-safe configuration:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `year` | int | 2022 | Tax year (2018-2025 supported) |
| `is_married` | bool | False | Married status (Ehegattensplitting) |
| `has_children` | bool | False | Has children (affects nursing insurance) |
| `church_tax` | float | 0.09 | Church tax rate (0.0-0.09, set to 0.0 for none) |
| `extra_health_insurance` | float | 0.014 | Additional health insurance rate |

## Supported Tax Years

| Year | Status | Notes |
|------|--------|-------|
| 2018-2022 | ✅ Fully supported | Complete tax data |
| 2023-2025 | ✅ Fully supported | Complete tax data |
| 2026-2027 | 📋 Planned | To be added |

## Documentation

Full documentation is available at [netto.readthedocs.io](https://netto.readthedocs.io/).

## Data Sources

All tax calculations are based on official German government sources:

- **Tax Calculation Formulas**: [BMF Tarifhistorie](https://www.bmf-steuerrechner.de/Tarifhistorie_Steuerrechner.pdf)
- **Wage Tax Calculator**: [BMF Lohnsteuerrechner](https://www.bmf-steuerrechner.de/)
- **Social Security Deductible**: [Vorsorgepauschale](https://www.lohn-info.de/vorsorgepauschale.html)
- **Social Security Rates**: [Sozialversicherungsbeiträge](https://www.lohn-info.de/sozialversicherungsbeitraege2024.html)
- **Solidarity Tax**: [Solidaritätszuschlag](https://www.lohn-info.de/solizuschlag.html)
- **Taxable Income Calculator**: [Reverse Calculator](https://udo-brechtel.de/mathe/est_gsv/reverse_zve_brutto.htm)

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/0-k/netto.git
cd netto

# Install in development mode with dev dependencies
pip install -e .
pip install -r requirements-dev.txt

# Set up pre-commit hooks (recommended)
pre-commit install
```

Pre-commit hooks automatically run ruff linting and formatting before each commit, preventing CI failures.

### Running Tests

```bash
# First-time setup: install package in editable mode
pip install -e .

# Run all tests with coverage
python -m pytest --cov=netto test/

# Run specific test file
python -m pytest test/test_main.py -v
```

**Note**: Use `python -m pytest` (not just `pytest`) to ensure tests run in the correct Python environment where netto is installed.

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Fix linting issues automatically
ruff check --fix .
```

### Building Documentation

```bash
cd docs/
make html
# Open docs/_build/html/index.html in your browser
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created and maintained by Martin Klein (hi@martinklein.co).

**Repository**: https://github.com/0-k/netto
**Documentation**: https://netto.readthedocs.io/
**PyPI**: https://pypi.org/project/netto/

---

© 2025 Martin Klein
