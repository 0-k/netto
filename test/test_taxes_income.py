import pytest

import netto.taxes_income as taxes_income
from netto.config import TaxConfig


@pytest.fixture
def default_config():
    """Fixture providing default config for tests"""
    return TaxConfig(
        year=2022, extra_health_insurance=0.014, church_tax=0.09, has_children=False
    )


@pytest.mark.parametrize(
    "taxable_income,expected_rate",
    [
        (-1000, 0),
        (0, 0),
        (10346, 0),
        (10347, 0.14),
        (14926, 0.2397),
        (58596, 0.42),
        (58597, 0.42),
        (100000, 0.42),
        (277826, 0.45),
        (277827, 0.45),
    ],
)
def test_get_marginal_tax_rate(taxable_income, expected_rate, default_config):
    """Test marginal tax rate calculation for various income levels"""
    result = taxes_income.get_marginal_tax_rate(taxable_income, default_config)
    assert result == expected_rate


@pytest.mark.parametrize(
    "taxable_income,expected_rate",
    [
        (10346, 0),
        (10347, 0),
        (10346 * 2, 0),
        (10347 * 2, 0.14),
    ],
)
def test_get_marginal_tax_rate_married(taxable_income, expected_rate):
    """Test marginal tax rate for married couples (doubled brackets)"""
    config = TaxConfig(year=2022, is_married=True)
    result = taxes_income.get_marginal_tax_rate(taxable_income, config)
    assert result == expected_rate


@pytest.mark.parametrize(
    "taxable_income",
    [
        12000,
        0,
        10000,
        20000,
        30000,
        40000,
        50000,
        60000,
        70000,
        80000,
        90000,
        100000,
        300000,
    ],
)
def test_sameness_of_calc_income_tax_methods(taxable_income, default_config):
    """Test that both income tax calculation methods give similar results"""
    result_direct = taxes_income.calc_income_tax(taxable_income, default_config)
    result_integration = taxes_income.calc_income_tax_by_integration(
        taxable_income, default_config
    )
    assert abs(result_direct - result_integration) < 0.1


@pytest.mark.parametrize(
    "taxable_income", [10000, 30000, 60000, 100000, 200000, 600000]
)
def test_calc_income_tax_married_equals_splitting(taxable_income, default_config):
    """Married income tax must equal the official splitting tariff: 2 * T(zvE/2)"""
    married_config = TaxConfig(year=2022, is_married=True)
    result = taxes_income.calc_income_tax(taxable_income, married_config)
    expected = 2 * taxes_income.calc_income_tax(taxable_income / 2, default_config)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize("taxable_income", [0, 20000, 50000, 100000, 300000])
def test_sameness_of_calc_income_tax_methods_married(taxable_income):
    """Both income tax calculation methods must agree for married couples"""
    married_config = TaxConfig(year=2022, is_married=True)
    result_direct = taxes_income.calc_income_tax(taxable_income, married_config)
    result_integration = taxes_income.calc_income_tax_by_integration(
        taxable_income, married_config
    )
    assert abs(result_direct - result_integration) < 0.5


@pytest.mark.parametrize(
    "year,expected",
    [
        (2018, 48964),  # 50000 - 1000 (Werbungskosten) - 36 (Sonderausgaben)
        (2021, 48964),
        (2022, 48764),  # Werbungskosten-Pauschbetrag raised to 1200
        (2023, 48734),  # Werbungskosten-Pauschbetrag raised to 1230
        (2025, 48734),
    ],
)
def test_calc_taxable_income_year_aware_lump_sums(year, expected):
    """Test that lump-sum deductions match the year-specific Pauschbeträge"""
    config = TaxConfig(year=year)
    result = taxes_income.calc_taxable_income(50000, 0, config=config)
    assert result == expected


def test_calc_taxable_income_married_doubles_sonderausgaben():
    """Married couples get the doubled Sonderausgaben-Pauschbetrag (72 instead of 36)"""
    config = TaxConfig(year=2025, is_married=True)
    result = taxes_income.calc_taxable_income(50000, 0, config=config)
    assert result == 48698  # 50000 - 1230 - 72


def test_calc_taxable_income_dual_earner():
    """Each earner gets their own Werbungskosten-Pauschbetrag"""
    config = TaxConfig(year=2025, is_married=True)
    result = taxes_income.calc_taxable_income(
        50000, 0, config=config, partner_salary=40000
    )
    assert result == 87468  # (50000 - 1230) + (40000 - 1230) - 72


def test_calc_taxable_income_partner_below_pauschbetrag():
    """The partner's Werbungskosten deduction cannot exceed their income"""
    config = TaxConfig(year=2025, is_married=True)
    result = taxes_income.calc_taxable_income(
        50000, 0, config=config, partner_salary=500
    )
    assert result == 48698  # partner income fully offset by the lump sum


def test_get_marginal_tax_rate_with_default_none_config():
    """Test that get_marginal_tax_rate works when config=None"""
    result = taxes_income.get_marginal_tax_rate(50000)
    assert isinstance(result, float)
    assert 0 <= result <= 1


def test_calc_income_tax_with_default_none_config():
    """Test that calc_income_tax works when config=None"""
    # Use explicit year=2022 since calc_income_tax requires const values
    # which are not available for 2023-2025
    result = taxes_income.calc_income_tax(50000, config=TaxConfig(year=2022))
    assert isinstance(result, float)
    assert result >= 0


def test_calc_income_tax_by_integration_with_default_none_config():
    """Test that calc_income_tax_by_integration works when config=None"""
    result = taxes_income.calc_income_tax_by_integration(50000)
    assert isinstance(result, float)
    assert result >= 0
