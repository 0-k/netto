# Tax and Social Security Data

This directory contains all tax and social security data used by the netto calculator in JSON format.

## Directory Structure

```
data/
├── tax_curves/          # Income tax curves by year
│   ├── 2018.json
│   ├── 2019.json
│   ├── ...
│   └── 2025.json
├── social_security/     # Social security rates by year
│   ├── 2018.json
│   ├── 2019.json
│   ├── ...
│   └── 2025.json
├── soli/                # Solidarity tax parameters by year
│   ├── 2018.json
│   ├── 2019.json
│   ├── ...
│   └── 2025.json
├── pension_factors/     # Pension deduction factors by year
│   ├── 2018.json
│   ├── 2019.json
│   ├── ...
│   └── 2025.json
└── README.md           # This file
```

## Data Format

### Tax Curves (`tax_curves/YEAR.json`)

Each file contains the progressive income tax brackets for a specific year:

```json
{
  "year": 2022,
  "brackets": {
    "0": {
      "step": 10347,
      "rate": 0.14,
      "const": null
    },
    "1": {
      "step": 14926,
      "rate": 0.2397,
      "const": [1088.67, 1400]
    },
    "2": {
      "step": 58596,
      "rate": 0.42,
      "const": [206.43, 2397, 869.32]
    },
    "3": {
      "step": 277826,
      "rate": 0.45,
      "const": [9336.45, 17671.20]
    }
  }
}
```

**Fields:**
- `year`: Tax year
- `brackets`: Four brackets (0-3) representing German progressive tax system
  - `step`: Income threshold in EUR where this bracket starts
  - `rate`: Tax rate for this bracket (as decimal, e.g., 0.14 = 14%)
  - `const`: Polynomial coefficients used in German tax formula
    - Bracket 0: `null` (no tax below basic allowance)
    - Bracket 1: `[a, b]` - 2 coefficients
    - Bracket 2: `[a, b, c]` - 3 coefficients
    - Bracket 3: `[a, b]` - 2 coefficients

**Note:** For years 2023-2025, `const` values are currently `null` and need to be filled in from official BMF sources.

### Social Security (`social_security/YEAR.json`)

Each file contains social security contribution limits and rates:

```json
{
  "year": 2022,
  "pension": {
    "limit": 84600,
    "rate": 0.093
  },
  "unemployment": {
    "limit": 84600,
    "rate": 0.012
  },
  "health": {
    "limit": 58050,
    "rate": 0.073
  },
  "nursing": {
    "limit": 58050,
    "rate": 0.01525,
    "extra": 0.0035
  }
}
```

**Fields:**
- `year`: Tax year
- `pension/unemployment/health/nursing`: Contribution type
  - `limit`: Annual income limit in EUR (Beitragsbemessungsgrenze)
  - `rate`: Employee contribution rate (employer pays the same)
  - `extra`: Extra rate for childless individuals (nursing only)

### Solidarity Tax (`soli/YEAR.json`)

Each file contains solidarity tax (Solidaritätszuschlag) parameters for a specific year:

```json
{
  "year": 2022,
  "start_taxable_income": 16956,
  "start_fraction": 0.119,
  "end_rate": 0.055
}
```

**Fields:**
- `year`: Tax year
- `start_taxable_income`: Income threshold in EUR where soli starts
- `start_fraction`: Fraction used for progressive phase-in
- `end_rate`: Maximum soli rate (5.5%)

**Important Change in 2021:** Solidarity tax was significantly reduced. Before 2021, it applied to most taxpayers. From 2021 onward, it only affects high earners through a progressive phase-in mechanism.

### Pension Correction Factors (`pension_factors/YEAR.json`)

Each file contains pension deduction factor for West Germany for a specific year:

```json
{
  "year": 2022,
  "factor": 0.88
}
```

**Fields:**
- `year`: Tax year
- `factor`: Pension deduction factor (0.0 to 1.0)

**Note:** These factors gradually increase each year, reaching 100% deductibility (1.0) in 2025.

## Data Sources

All data should be sourced from official German government sources:

- **Tax formulas:** [BMF Tarifhistorie](https://www.bmf-steuerrechner.de/Tarifhistorie_Steuerrechner.pdf)
- **Tax calculators:** [BMF Lohnsteuerrechner](https://www.bmf-steuerrechner.de/)
- **Social security rates:** [Sozialversicherungsbeiträge](https://www.lohn-info.de/sozialversicherungsbeitraege2024.html)
- **Soli:** [Solidaritätszuschlag](https://www.lohn-info.de/solizuschlag.html)

## Validation

All JSON data is validated using Pydantic models defined in `netto/data_loader.py`. The validation ensures:

- Correct data types (floats, integers, arrays)
- Proper value ranges (e.g., rates between 0 and 1)
- Required fields are present
- Structural integrity (e.g., exactly 4 tax brackets)

## Adding New Years

To add tax data for a new year:

1. **Create tax curve file:** `tax_curves/YEAR.json`
   - Source data from BMF Tarifhistorie
   - Calculate `const` polynomial coefficients from official formulas

2. **Create social security file:** `social_security/YEAR.json`
   - Source limits (Beitragsbemessungsgrenzen) from official sources
   - Source rates from official announcements

3. **Create soli file:** `soli/YEAR.json`
   - Add year entry with updated thresholds

4. **Create pension factor file:** `pension_factors/YEAR.json`
   - Add year entry with factor (continues at 1.0 after 2025)

5. **Update validation in** `netto/config.py`:
   - Update year range validation

6. **Run tests:**
   - Verify calculations against official BMF calculator
   - Add test cases for new year

## Maintenance

- Data files are version controlled separately for easy auditing
- Each change should reference the official source
- Use conventional commit format: `data: update 2024 social security rates`
- Verify calculations against official calculators before committing

## Current Status

| Year | Tax Curve | Social Security | Soli | Pension Factor | Status |
|------|-----------|-----------------|------|----------------|--------|
| 2018 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | Fully supported |
| 2019 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | Fully supported |
| 2020 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | Fully supported |
| 2021 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | Fully supported |
| 2022 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | Fully supported |
| 2023 | ⚠️ Partial | ✅ Complete | ✅ Complete | ✅ Complete | Missing `const` coefficients |
| 2024 | ⚠️ Partial | ✅ Complete | ✅ Complete | ✅ Complete | Missing `const` coefficients |
| 2025 | ⚠️ Partial | ✅ Complete | ✅ Complete | ✅ Complete | Missing `const` coefficients |
| 2026 | ❌ Missing | ❌ Missing | ❌ Missing | To be decided | Not yet available |
| 2027 | ❌ Missing | ❌ Missing | ❌ Missing | To be decided | Not yet available |

**Priority:** Complete `const` coefficients for 2023-2025 tax curves for release 0.2.0.
