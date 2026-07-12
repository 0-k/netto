import pytest

import netto.main as main
import netto.social_security as social_security
import netto.taxes_children as taxes_children
import netto.taxes_income as taxes_income
from netto.config import TaxConfig


@pytest.fixture
def married_two_kids():
    """Married couple with two children, no church tax, 2026"""
    return TaxConfig(year=2026, is_married=True, num_children=2, church_tax=0.0)


@pytest.fixture
def married_childless_reference():
    """Same as married_two_kids but children only via has_children
    (nursing surcharge removed, no Kindergeld/Freibetrag)"""
    return TaxConfig(year=2026, is_married=True, has_children=True, church_tax=0.0)


@pytest.mark.parametrize(
    "year,expected_per_child",
    [
        (2018, 2328),
        (2019, 2388),  # July increase: 6 x 194 + 6 x 204
        (2023, 3000),
        (2025, 3060),
        (2026, 3108),
    ],
)
def test_calc_kindergeld_per_year(year, expected_per_child):
    """Kindergeld matches the official yearly amounts (first/second child)"""
    config = TaxConfig(year=year, num_children=1)
    assert taxes_children.calc_kindergeld(config) == expected_per_child


def test_calc_kindergeld_scales_with_children():
    config = TaxConfig(year=2026, num_children=3)
    assert taxes_children.calc_kindergeld(config) == 3 * 3108


def test_calc_kindergeld_zero_without_children():
    assert taxes_children.calc_kindergeld(TaxConfig(year=2026)) == 0


def test_child_allowance_halved_for_singles():
    """Single parents get half the allowance (other half belongs to the
    other parent)"""
    married = TaxConfig(year=2026, is_married=True, num_children=1)
    single = TaxConfig(year=2026, num_children=1)
    assert taxes_children.calc_child_allowance_per_child(married) == 9756
    assert taxes_children.calc_child_allowance_per_child(single) == 9756 / 2


def test_guenstigerpruefung_kindergeld_wins_at_low_income(
    married_two_kids, married_childless_reference
):
    """At low income the allowance relief is below the Kindergeld, so the
    net benefit is exactly the Kindergeld"""
    netto_kids = main.calc_netto(30000, config=married_two_kids)
    netto_ref = main.calc_netto(30000, config=married_childless_reference)
    kindergeld = taxes_children.calc_kindergeld(married_two_kids)
    assert netto_kids - netto_ref == pytest.approx(kindergeld, abs=0.02)


def test_guenstigerpruefung_freibetrag_wins_at_high_income(
    married_two_kids, married_childless_reference
):
    """At high income the allowance relief exceeds the Kindergeld, so the
    net benefit is larger than the Kindergeld"""
    netto_kids = main.calc_netto(150000, config=married_two_kids, partner_salary=80000)
    netto_ref = main.calc_netto(
        150000, config=married_childless_reference, partner_salary=80000
    )
    kindergeld = taxes_children.calc_kindergeld(married_two_kids)
    assert netto_kids - netto_ref > kindergeld


def test_child_benefit_never_below_kindergeld(
    married_two_kids, married_childless_reference
):
    """The Günstigerprüfung guarantees at least the Kindergeld"""
    kindergeld = taxes_children.calc_kindergeld(married_two_kids)
    for salary in [0, 20000, 50000, 100000, 200000, 400000]:
        netto_kids = main.calc_netto(salary, config=married_two_kids)
        netto_ref = main.calc_netto(salary, config=married_childless_reference)
        assert netto_kids - netto_ref >= kindergeld - 0.02


def test_soli_and_church_tax_use_fictitious_tax():
    """Soli and church tax are based on the income tax with child
    allowances deducted, which is lower than the regular income tax"""
    config = TaxConfig(year=2026, is_married=True, num_children=2)
    taxable_income = 200000
    income_tax = taxes_income.calc_income_tax_by_integration(taxable_income, config)
    assessed, fictitious = taxes_children.apply_guenstigerpruefung(
        taxable_income, income_tax, config
    )
    assert fictitious < income_tax
    # at this income the Freibetrag wins, so the assessed tax reflects the
    # allowance deduction plus the Kindergeld Hinzurechnung
    kindergeld = taxes_children.calc_kindergeld(config)
    assert assessed == pytest.approx(fictitious + kindergeld, abs=0.02)


def test_apply_guenstigerpruefung_no_children_passthrough():
    config = TaxConfig(year=2026, is_married=True)
    assessed, fictitious = taxes_children.apply_guenstigerpruefung(
        100000, 25000.0, config
    )
    assert assessed == 25000.0
    assert fictitious == 25000.0


def test_num_children_implies_has_children():
    """num_children > 0 removes the nursing childless surcharge"""
    config = TaxConfig(year=2026, num_children=2)
    assert config.has_children is True
    reference = TaxConfig(year=2026, has_children=True)
    assert social_security.calc_social_security(
        50000, config
    ) == social_security.calc_social_security(50000, reference)


def test_zero_gross_yields_kindergeld(married_two_kids):
    """A household without salary still receives the Kindergeld"""
    assert main.calc_netto(0, config=married_two_kids) == pytest.approx(
        taxes_children.calc_kindergeld(married_two_kids)
    )


def test_num_children_validation():
    with pytest.raises(ValueError):
        TaxConfig(num_children=-1)
    with pytest.raises(TypeError):
        TaxConfig(num_children=2.0)
    with pytest.raises(TypeError):
        TaxConfig(num_children=True)


def test_forecast_years_have_child_data():
    """Child benefits are available for all supported years incl. forecasts"""
    for year in range(2018, 2033):
        config = TaxConfig(year=year, num_children=1)
        assert taxes_children.calc_kindergeld(config) > 0
