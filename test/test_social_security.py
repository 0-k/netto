import pytest

import netto.social_security as social_security
from netto.config import TaxConfig


@pytest.fixture
def default_config():
    """Fixture providing default config for tests"""
    return TaxConfig(
        year=2022, extra_health_insurance=0.014, church_tax=0.09, has_children=False
    )


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (10000, 0.093),
        (84600, 0.093),
        (84601, 0),
        (100000, 0),
    ],
)
def test_get_rate_pension(salary, expected, default_config):
    """Test pension rate calculation"""
    result = social_security.get_rate_pension(salary, default_config)
    assert result == expected


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (10000, 0.08),
        (58050, 0.08),
        (58051, 0),
        (100000, 0),
    ],
)
def test_get_rate_health(salary, expected, default_config):
    """Test health insurance rate calculation"""
    result = social_security.get_rate_health(salary, default_config)
    assert result == expected


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (10000, 0.093 * 10000),
        (84600, 0.093 * 84600),
        (84601, 0.093 * 84600),
        (100000, 0.093 * 84600),
    ],
)
def test_calc_insurance_pension(salary, expected, default_config):
    """Test pension insurance calculation"""
    result = social_security.calc_insurance_pension(salary, default_config)
    assert result == expected


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (10000, 0.08 * 10000),
        (58050, 0.08 * 58050),
        (58051, 0.08 * 58050),
        (100000, 0.08 * 58050),
    ],
)
def test_calc_insurance_health(salary, expected, default_config):
    """Test health insurance calculation"""
    result = social_security.calc_insurance_health(salary, default_config)
    assert result == expected


def test_calc_deductible_social_security(default_config):
    """Test deductible social security calculation"""
    assert social_security.calc_deductible_social_security(0, default_config) == 0
    # https://www.lohn-info.de/vorsorgepauschale.html
    assert (
        social_security.calc_deductible_social_security(30000, default_config)
        == 2456 + 2310 + 563
    )


@pytest.mark.parametrize(
    "salary", [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
)
def test_sameness_of_calc_social_security(salary, default_config):
    """Test that both social security calculation methods give same results"""
    result_direct = social_security.calc_social_security(salary, default_config)
    result_integration = social_security.calc_social_security_by_integration(
        salary, default_config
    )
    assert result_direct == result_integration


@pytest.mark.parametrize(
    "salary", [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
)
def test_sameness_of_calc_social_security_different_config(salary):
    """Test social security calculation with different config"""
    config = TaxConfig(extra_health_insurance=0.015, has_children=True)
    result_direct = social_security.calc_social_security(salary, config)
    result_integration = social_security.calc_social_security_by_integration(
        salary, config
    )
    assert abs(result_direct - result_integration) < 0.02


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (10000, 0.0805),
        (58050, 0.0805),
        (58051, 0),
        (100000, 0),
    ],
)
def test_get_rate_health_different_config(salary, expected):
    """Test health rate with different extra health insurance"""
    config = TaxConfig(year=2022, extra_health_insurance=0.015)
    result = social_security.get_rate_health(salary, config)
    assert abs(result - expected) < 0.0001


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (10000, 0.01875),
        (58050, 0.01875),
        (58051, 0),
        (100000, 0),
    ],
)
def test_get_rate_nursing_no_children(salary, expected):
    """Test nursing rate without children (includes extra rate)"""
    config = TaxConfig(year=2022, has_children=False)
    result = social_security.get_rate_nursing(salary, config)
    assert result == expected


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (10000, 0.01525),
        (58050, 0.01525),
        (58051, 0),
        (100000, 0),
    ],
)
def test_get_rate_nursing_with_children(salary, expected):
    """Test nursing rate with children (no extra rate)"""
    config = TaxConfig(year=2022, has_children=True)
    result = social_security.get_rate_nursing(salary, config)
    assert result == expected


def test_get_rate_pension_with_default_none_config():
    """Test that get_rate_pension works when config=None"""
    result = social_security.get_rate_pension(50000)
    assert isinstance(result, float)
    assert result >= 0


def test_get_rate_unemployment_with_default_none_config():
    """Test that get_rate_unemployment works when config=None"""
    result = social_security.get_rate_unemployment(50000)
    assert isinstance(result, float)
    assert result >= 0


def test_get_rate_health_with_default_none_config():
    """Test that get_rate_health works when config=None"""
    result = social_security.get_rate_health(50000)
    assert isinstance(result, float)
    assert result >= 0


def test_get_rate_nursing_with_default_none_config():
    """Test that get_rate_nursing works when config=None"""
    result = social_security.get_rate_nursing(50000)
    assert isinstance(result, float)
    assert result >= 0


def test_calc_insurance_pension_with_default_none_config():
    """Test that calc_insurance_pension works when config=None"""
    result = social_security.calc_insurance_pension(50000)
    assert isinstance(result, float)
    assert result >= 0


def test_calc_insurance_health_with_default_none_config():
    """Test that calc_insurance_health works when config=None"""
    result = social_security.calc_insurance_health(50000)
    assert isinstance(result, float)
    assert result >= 0


def test_calc_social_security_with_default_none_config():
    """Test that calc_social_security works when config=None"""
    result = social_security.calc_social_security(50000)
    assert isinstance(result, float)
    assert result >= 0


def test_calc_deductible_social_security_with_default_none_config():
    """Test that calc_deductible_social_security works when config=None"""
    result = social_security.calc_deductible_social_security(50000)
    assert isinstance(result, int | float)
    assert result >= 0
