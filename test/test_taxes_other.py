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
