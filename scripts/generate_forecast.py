"""
Generate forecast tax data for future years (2027-2032).

All generated values are ESTIMATES for planning purposes, extrapolated from
enacted 2026 law. Assumptions (edit below and re-run to regenerate):

Income tax curve
    - Bracket boundaries E0 (Grundfreibetrag), E1, E2 are indexed by
      TARIFF_INDEXATION per year, following the pattern of recent
      inflation-adjustment laws (2025->2026 was ~+2.1%).
    - The top bracket boundary E3 (277,826) stays frozen, as it has been
      since 2022 (deliberate policy).
    - Polynomial coefficients are derived exactly from the boundaries using
      the structure of § 32a EStG (marginal rate rises linearly from 14% to
      23.97% in zone 1 and from 23.97% to 42% in zone 2).

Solidarity tax
    - Exemption threshold indexed by TARIFF_INDEXATION per year.

Social security
    - Contribution ceilings (Beitragsbemessungsgrenzen) grow by BBG_GROWTH
      per year (long-run wage growth; 2018-2026 average was ~3.3%), rounded
      to the official grid (multiples of 600 EUR/year for pension and
      unemployment, 150 EUR/year for health and nursing).
    - Pension rate follows the official Rentenversicherungsbericht
      projection: stable at 18.6% until 2027, then rising towards ~20% by
      the early 2030s (employee half in PENSION_RATE_PATH).
    - Nursing rate rises moderately (PFLEGE_RATE_PATH), reflecting projected
      financing gaps; childless surcharge unchanged.
    - The average health Zusatzbeitrag (health "extra") keeps rising by
      0.1 percentage points per year (HEALTH_EXTRA_PATH), continuing the
      trend that reached 2.9% in 2026.
    - Health base (7.3%) and unemployment (1.3%) employee rates stay flat.

Lump-sum deductions and pension deduction factor
    - Werbungskosten-Pauschbetrag (1,230) and Sonderausgaben-Pauschbetrag
      (36) stay flat (no enacted changes).
    - Pension contributions remain 100% deductible (factor 1.0, law since
      2023).

Child benefits
    - Kindergeld and Kinderfreibetrag (incl. BEA) are indexed by
      TARIFF_INDEXATION per year, rounded to multiples of 12 EUR/year so
      monthly amounts stay whole euros.

Run from the repository root:  python scripts/generate_forecast.py
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

FORECAST_YEARS = range(2027, 2033)

TARIFF_INDEXATION = 0.02  # yearly growth of tax bracket boundaries and soli threshold
BBG_GROWTH = 0.03  # yearly growth of social security contribution ceilings
E3_FROZEN = 277826  # top bracket boundary, frozen since 2022

# Employee shares; pension per Rentenversicherungsbericht projection path
PENSION_RATE_PATH = {
    2027: 0.093,
    2028: 0.094,
    2029: 0.096,
    2030: 0.098,
    2031: 0.099,
    2032: 0.100,
}
PFLEGE_RATE_PATH = {
    2027: 0.018,
    2028: 0.019,
    2029: 0.019,
    2030: 0.020,
    2031: 0.020,
    2032: 0.020,
}
# Total average Zusatzbeitrag (not halved); 2026 official average was 2.9%
HEALTH_EXTRA_PATH = {
    2027: 0.030,
    2028: 0.031,
    2029: 0.032,
    2030: 0.033,
    2031: 0.034,
    2032: 0.035,
}


def derive_tax_constants(e0: int, e1: int, e2: int, e3: int) -> dict:
    """Derive § 32a EStG polynomial coefficients from bracket boundaries.

    Zone 1 (E0..E1): marginal rate rises linearly 14% -> 23.97%,
    tax = (a*y + 1400)*y with y = (zvE - E0)/10000.
    Zone 2 (E1..E2): marginal rate rises linearly 23.97% -> 42%,
    tax = (b*z + 2397)*z + C with z = (zvE - E1)/10000.
    Zones 3/4: tax = 0.42*zvE - s0 and 0.45*zvE - s1.
    """
    a = 4985000 / (e1 - e0)  # (2397 - 1400) * 10000 / (2 * (E1 - E0))
    tax_at_e1 = 1898.5 * (e1 - e0) / 10000  # (a*y1 + 1400)*y1 simplified
    b = 9015000 / (e2 - e1)  # (4200 - 2397) * 10000 / (2 * (E2 - E1))
    tax_at_e2 = tax_at_e1 + 3298.5 * (e2 - e1) / 10000
    s0 = 0.42 * e2 - tax_at_e2
    s1 = s0 + 0.03 * e3
    return {
        "0": {"step": e0, "rate": 0.14, "const": None},
        "1": {"step": e1, "rate": 0.2397, "const": [round(a, 2), 1400]},
        "2": {
            "step": e2,
            "rate": 0.42,
            "const": [round(b, 2), 2397, round(tax_at_e1, 2)],
        },
        "3": {"step": e3, "rate": 0.45, "const": [round(s0, 2), round(s1, 2)]},
    }


def round_to(value: float, grid: int) -> int:
    return int(round(value / grid) * grid)


def write_json(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"wrote {path}")


def main() -> None:
    base_tax = json.load(open(DATA_DIR / "tax_curves" / "2026.json"))["brackets"]
    e0 = base_tax["0"]["step"]
    e1 = base_tax["1"]["step"]
    e2 = base_tax["2"]["step"]

    base_soli = json.load(open(DATA_DIR / "soli" / "2026.json"))
    soli_threshold = base_soli["start_taxable_income"]

    base_social = json.load(open(DATA_DIR / "social_security" / "2026.json"))
    bbg_pension = base_social["pension"]["limit"]
    bbg_health = base_social["health"]["limit"]

    base_children = json.load(open(DATA_DIR / "children" / "2026.json"))
    kindergeld = base_children["kindergeld_per_child"]
    kinderfreibetrag = base_children["kinderfreibetrag_per_child"]

    for year in FORECAST_YEARS:
        e0 = round(e0 * (1 + TARIFF_INDEXATION))
        e1 = round(e1 * (1 + TARIFF_INDEXATION))
        e2 = round(e2 * (1 + TARIFF_INDEXATION))
        write_json(
            DATA_DIR / "tax_curves" / f"{year}.json",
            {"year": year, "brackets": derive_tax_constants(e0, e1, e2, E3_FROZEN)},
        )

        soli_threshold = round(soli_threshold * (1 + TARIFF_INDEXATION))
        write_json(
            DATA_DIR / "soli" / f"{year}.json",
            {
                "year": year,
                "start_taxable_income": soli_threshold,
                "start_fraction": 0.119,
                "end_rate": 0.055,
            },
        )

        bbg_pension = round_to(bbg_pension * (1 + BBG_GROWTH), 600)
        bbg_health = round_to(bbg_health * (1 + BBG_GROWTH), 150)
        write_json(
            DATA_DIR / "social_security" / f"{year}.json",
            {
                "year": year,
                "pension": {"limit": bbg_pension, "rate": PENSION_RATE_PATH[year]},
                "unemployment": {"limit": bbg_pension, "rate": 0.013},
                "health": {
                    "limit": bbg_health,
                    "rate": 0.073,
                    "extra": HEALTH_EXTRA_PATH[year],
                },
                "nursing": {
                    "limit": bbg_health,
                    "rate": PFLEGE_RATE_PATH[year],
                    "extra": 0.006,
                },
            },
        )

        write_json(
            DATA_DIR / "pension_factors" / f"{year}.json",
            {"year": year, "factor": 1.0},
        )

        write_json(
            DATA_DIR / "deductions" / f"{year}.json",
            {
                "year": year,
                "werbungskosten_pauschbetrag": 1230,
                "sonderausgaben_pauschbetrag": 36,
            },
        )

        kindergeld = round_to(kindergeld * (1 + TARIFF_INDEXATION), 12)
        kinderfreibetrag = round_to(kinderfreibetrag * (1 + TARIFF_INDEXATION), 12)
        write_json(
            DATA_DIR / "children" / f"{year}.json",
            {
                "year": year,
                "kindergeld_per_child": kindergeld,
                "kinderfreibetrag_per_child": kinderfreibetrag,
            },
        )


if __name__ == "__main__":
    main()
