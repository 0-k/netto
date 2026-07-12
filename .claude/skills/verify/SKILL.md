---
name: verify
description: Verify netto library changes by driving the public package API end-to-end
---

# Verifying netto changes

netto is a pure-Python library; its surface is the public package boundary
(`from netto import calc_netto, calc_inverse_netto, TaxConfig`).

## Handle

- `pip install -e .` (usually already installed; check with
  `python -c "import netto; print(netto.__file__)"`).
- Drive it with a consumer script run from OUTSIDE the repo (e.g. the session
  scratchpad) so imports resolve through the installed package, plus
  `python examples/examples.py` from the repo root as the in-repo consumer.

## Flows worth driving

- `calc_netto` across years (2018, 2022, 2025) and configs: single, married,
  `partner_salary` (dual income), `verbose=True`, church tax on/off.
- `calc_inverse_netto` roundtrip: `calc_inverse_netto(calc_netto(x)) == x`.
- Married invariants: netto(married) >= netto(single);
  household netto symmetric under swapping salary/partner_salary;
  soli 0 below the doubled Freigrenze.
- Error paths: negative salary/partner_salary, partner_salary without
  is_married, desired netto already covered by partner salary alone.

## Gotchas

- `ruff format .` from the repo root also formats files in the cwd — run the
  consumer script from the scratchpad, not the repo.
- scipy emits an IntegrationWarning for very high incomes (>= ~300k); it is
  pre-existing and harmless.
- Cross-check income tax against the official formula: for married,
  `calc_income_tax(zvE, married)` must equal `2 * calc_income_tax(zvE/2, single)`
  (`calc_income_tax` implements the exact BMF polynomial).
