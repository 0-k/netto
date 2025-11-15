from io import StringIO
from unittest.mock import patch

import pytest

import netto.main as main
from netto.config import TaxConfig


@pytest.fixture
def default_config():
    """Fixture providing default config for tests"""
    return TaxConfig(extra_health_insurance=0.014, church_tax=0.09, has_children=False)


@pytest.fixture
def alternate_config():
    """Fixture providing alternate config for tests"""
    return TaxConfig(extra_health_insurance=0.015, church_tax=0.0, has_children=True)


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (30000, 20554.38),
        (60000, 35796.68),
        (90000, 49956.92),
        (120000, 64965.08),
    ],
)
def test_calc_netto_with_default_config(salary, expected, default_config):
    """Test calc_netto with various salaries using default config"""
    result = main.calc_netto(salary, config=default_config)
    assert abs(result - expected) < 1


@pytest.mark.parametrize(
    "salary,expected",
    [
        (30000, 20894.58),
        (60000, 36909.71),
        (90000, 52091.39),
        (120000, 68238.23),
    ],
)
def test_calc_netto_with_alternate_config(salary, expected, alternate_config):
    """Test calc_netto with alternate config (no church tax, with children)"""
    result = main.calc_netto(salary, config=alternate_config)
    assert abs(result - expected) < 1


@pytest.mark.parametrize(
    "desired_netto,expected_gross",
    [
        (20894.58, 30000),
        (36909.71, 60000),
        (52091.39, 90000),
        (68238.23, 120000),
    ],
)
def test_calc_inverse_netto(desired_netto, expected_gross, alternate_config):
    """Test inverse netto calculation"""
    result = main.calc_inverse_netto(desired_netto, config=alternate_config)
    assert abs(result - expected_gross) <= 1


def test_calc_inverse_netto_roundtrip(alternate_config):
    """Test that calc_inverse_netto and calc_netto are inverses"""
    salary = 10000
    netto = main.calc_netto(salary, config=alternate_config)
    gross = main.calc_inverse_netto(netto, config=alternate_config)
    assert gross == salary


@patch("sys.stdout", new_callable=StringIO)
def test_verbose_print(mock_stdout, default_config):
    """Test that verbose mode prints expected output"""
    main.calc_netto(0, verbose=True, config=default_config)
    actual_output = mock_stdout.getvalue().strip()
    expected_output = (
        "Yearly Evaluation:\n"
        + f"Income Tax:      {0.0:>12}\n"
        + f"Soli:            {0.0:>12}\n"
        + f"Church Tax:      {0.0:>12}\n"
        + f"Social Security: {0.0:>12}"
    )
    assert actual_output == expected_output


def test_calc_netto_with_default_none_config():
    """Test that calc_netto works when config=None (uses default TaxConfig)"""
    result = main.calc_netto(30000)
    # Should use default TaxConfig (year=2022, etc.)
    assert isinstance(result, float)
    assert result > 0


def test_calc_inverse_netto_with_default_none_config():
    """Test that calc_inverse_netto works when config=None (uses default TaxConfig)"""
    # Use a value that we know works well with Newton's method
    result = main.calc_inverse_netto(30000)
    # Should use default TaxConfig
    assert isinstance(result, (int, float))
    assert result > 0
    # Verify the result makes sense (gross should be higher than net)
    assert result > 30000
