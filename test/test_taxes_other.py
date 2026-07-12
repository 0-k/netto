import pytest

import netto.taxes_other as taxes_other
from netto.config import TaxConfig


@pytest.fixture
def default_config():
    """Fixture providing default config for tests"""
    return TaxConfig(
        year=2022, extra_health_insurance=0.014, church_tax=0.09, has_children=False
    )


@pytest.mark.parametrize(
    "income_tax,expected",
    [
        (-1000, 0),
        (0, 0),
        (16956, 0),
        (100000, 5500),
    ],
)
def test_calc_soli_exact(income_tax, expected, default_config):
    """Test solidarity tax calculation with exact values"""
    result = taxes_other.calc_soli(income_tax, default_config)
    assert result == expected


@pytest.mark.parametrize(
    "income_tax,expected",
    [
        (16957, 0.119),
        (17514.96, 66.48),
        (26913.96, 1185.0),
    ],
)
def test_calc_soli_approximate(income_tax, expected, default_config):
    """Test solidarity tax calculation with approximate values"""
    result = taxes_other.calc_soli(income_tax, default_config)
    assert abs(result - expected) < 0.1


@pytest.mark.parametrize(
    "income_tax,expected",
    [
        (-1000, 0),
        (0, 0),
        (10000, 900),
    ],
)
def test_calc_church_tax(income_tax, expected, default_config):
    """Test church tax calculation"""
    result = taxes_other.calc_church_tax(income_tax, default_config)
    assert result == expected


@pytest.mark.parametrize(
    "income_tax,expected",
    [
        (33912, 0),  # doubled exemption threshold (2 * 16956) for joint assessment
        (33913, 0.12),
        (40000, 724.47),
        (100000, 5500),  # capped at 5.5% regardless of marital status
    ],
)
def test_calc_soli_married(income_tax, expected):
    """Test that the soli exemption threshold doubles for married couples"""
    config = TaxConfig(year=2022, is_married=True)
    result = taxes_other.calc_soli(income_tax, config)
    assert abs(result - expected) < 0.01


@pytest.mark.parametrize(
    "income_tax,expected",
    [
        (1944, 0),  # doubled exemption threshold (2 * 972) pre-2021
        (2000, 11.2),
        (100000, 5500),
    ],
)
def test_calc_soli_married_pre_2021(income_tax, expected):
    """Test married soli threshold doubling with pre-2021 parameters"""
    config = TaxConfig(year=2018, is_married=True)
    result = taxes_other.calc_soli(income_tax, config)
    assert abs(result - expected) < 0.01


def test_calc_soli_married_below_single_threshold_zone(default_config):
    """A tax amount above the single but below the married threshold
    must yield soli for singles but none for married couples"""
    income_tax = 30000  # 2022: single threshold 16956, married threshold 33912
    married_config = TaxConfig(year=2022, is_married=True)
    assert taxes_other.calc_soli(income_tax, default_config) > 0
    assert taxes_other.calc_soli(income_tax, married_config) == 0


def test_calc_soli_with_default_none_config():
    """Test that calc_soli works when config=None"""
    result = taxes_other.calc_soli(10000)
    assert isinstance(result, float)
    assert result >= 0


def test_calc_church_tax_with_default_none_config():
    """Test that calc_church_tax works when config=None"""
    result = taxes_other.calc_church_tax(10000)
    assert isinstance(result, float)
    assert result >= 0
