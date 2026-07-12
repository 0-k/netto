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
│   └── 2026.json
├── deductions/          # Lump-sum deductions (Pauschbeträge) by year
│   ├── 2018.json
│   ├── 2019.json
│   ├── ...
│   └── 2032.json
├── children/            # Kindergeld and Kinderfreibetrag by year
│   ├── 2018.json
│   ├── 2019.json
│   ├── ...
│   └── 2032.json
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
    "rate": 0.073,
    "extra": 0.013
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
  - `extra` (health): Official average Zusatzbeitrag for the year (total;
    the employee pays half). Used when `TaxConfig.extra_health_insurance`
    is `None`; an explicit config value overrides it.
  - `extra` (nursing): Extra rate for childless individuals
    (Kinderlosenzuschlag)

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

**Note:** These factors increased by 4 percentage points per year until the
Jahressteuergesetz 2022 brought full deductibility (1.0) forward to 2023
(originally scheduled for 2025).

### Lump-Sum Deductions (`deductions/YEAR.json`)

Each file contains the lump-sum deductions (Pauschbeträge) for a specific year:

```json
{
  "year": 2022,
  "werbungskosten_pauschbetrag": 1200,
  "sonderausgaben_pauschbetrag": 36
}
```

**Fields:**
- `year`: Tax year
- `werbungskosten_pauschbetrag`: Employee lump-sum deduction
  (Arbeitnehmer-Pauschbetrag) in EUR, granted per earner
  - 2018-2021: 1,000 €
  - 2022: 1,200 € (Steuerentlastungsgesetz 2022)
  - 2023 onwards: 1,230 €
- `sonderausgaben_pauschbetrag`: Special expenses lump sum in EUR per person
  (36 €, doubled to 72 € for jointly assessed couples)

### Child Benefits (`children/YEAR.json`)

Each file contains the yearly child benefit amounts for a specific year:

```json
{
  "year": 2026,
  "kindergeld_per_child": 3108,
  "kinderfreibetrag_per_child": 9756
}
```

**Fields:**
- `year`: Tax year
- `kindergeld_per_child`: Yearly Kindergeld in EUR at the first/second-child
  rate (mid-year changes are averaged in, e.g. 2019). Simplifications:
  before 2023 the third and further children received slightly more; one-off
  Corona-Kinderboni (2020-2022) are not included.
- `kinderfreibetrag_per_child`: Yearly child allowance in EUR for **both
  parents combined**, including the BEA allowance (Betreuungs-, Erziehungs-
  und Ausbildungsbedarf: 2,640 € until 2020, 2,928 € since 2021). Single
  parents receive half. The 2022 and 2024 values include the retroactive
  raises.

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

5. **Create deductions file:** `deductions/YEAR.json`
   - Add year entry with the current Pauschbeträge

6. **Create child benefits file:** `children/YEAR.json`
   - Add year entry with Kindergeld and Kinderfreibetrag (incl. BEA)

7. **Update validation in** `netto/config.py`:
   - Update year range validation

8. **Run tests:**
   - Verify calculations against official BMF calculator
   - Add test cases for new year

## Maintenance

- Data files are version controlled separately for easy auditing
- Each change should reference the official source
- Use conventional commit format: `data: update 2024 social security rates`
- Verify calculations against official calculators before committing

## Forecast Years (2027-2032)

The data files for 2027-2032 are **estimates for planning purposes**, generated
by `scripts/generate_forecast.py` from the enacted 2026 values. Assumptions:

- **Tax brackets and soli threshold**: indexed by 2% per year (matching recent
  inflation-adjustment laws); the top bracket boundary stays frozen at
  277,826 € as it has been since 2022. Polynomial coefficients are derived
  exactly from the bracket boundaries.
- **Contribution ceilings** (Beitragsbemessungsgrenzen): +3% per year
  (long-run wage growth), rounded to the official grid.
- **Pension rate**: follows the official Rentenversicherungsbericht projection
  (stable 18.6% until 2027, rising to ~20% by the early 2030s).
- **Nursing rate**: moderate increases reflecting projected financing gaps
  (3.6% → 4.0% total by 2030).
- **Average health Zusatzbeitrag**: keeps rising by 0.1 percentage points per
  year (2.9% in 2026 → 3.5% by 2032), continuing the recent trend.
- **Health base (14.6%) and unemployment (2.6%) rates, Pauschbeträge**: flat.
- **Kindergeld and Kinderfreibetrag**: indexed by 2% per year, rounded so
  monthly amounts stay whole euros.

To change assumptions, edit the constants at the top of
`scripts/generate_forecast.py` and re-run it. Replace forecast files with
official values as they are enacted.

## Current Status

| Year | Tax Curve | Social Security | Soli | Pension Factor | Deductions | Status |
|------|-----------|-----------------|------|----------------|------------|--------|
| 2018-2025 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | Fully supported |
| 2026 | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | ✅ Complete | Preliminary official data |
| 2027-2032 | 🔮 Forecast | 🔮 Forecast | 🔮 Forecast | 🔮 Forecast | 🔮 Forecast | Estimates (see above) |
