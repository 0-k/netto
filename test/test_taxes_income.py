import pytest

import netto.taxes_income as taxes_income
from netto.config import TaxConfig


@pytest.fixture
def default_config():
    """Fixture providing default config for tests"""
    return TaxConfig(extra_health_insurance=0.014, church_tax=0.09, has_children=False)


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
    config = TaxConfig(is_married=True)
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


def test_get_marginal_tax_rate_with_default_none_config():
    """Test that get_marginal_tax_rate works when config=None"""
    result = taxes_income.get_marginal_tax_rate(50000)
    assert isinstance(result, float)
    assert 0 <= result <= 1


def test_calc_income_tax_with_default_none_config():
    """Test that calc_income_tax works when config=None"""
    result = taxes_income.calc_income_tax(50000)
    assert isinstance(result, float)
    assert result >= 0


def test_calc_income_tax_by_integration_with_default_none_config():
    """Test that calc_income_tax_by_integration works when config=None"""
    result = taxes_income.calc_income_tax_by_integration(50000)
    assert isinstance(result, float)
    assert result >= 0
