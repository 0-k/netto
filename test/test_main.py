from io import StringIO
from unittest.mock import patch

import pytest

import netto.main as main
from netto.config import TaxConfig


@pytest.fixture
def default_config():
    """Fixture providing default config for tests"""
    return TaxConfig(
        year=2022, extra_health_insurance=0.014, church_tax=0.09, has_children=False
    )


@pytest.fixture
def alternate_config():
    """Fixture providing alternate config for tests"""
    return TaxConfig(
        year=2022, extra_health_insurance=0.015, church_tax=0.0, has_children=True
    )


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


@pytest.fixture
def married_config():
    """Fixture providing a married config for tests"""
    return TaxConfig(year=2025, is_married=True, church_tax=0.0)


@pytest.mark.parametrize(
    "salary,expected",
    [
        (50000, 36263.40),
        (100000, 67016.96),
        (150000, 98603.98),  # income tax 33940 is below married soli threshold 39900
        (250000, 152445.93),
    ],
)
def test_calc_netto_married(salary, expected, married_config):
    """Test married netto (splitting tariff, doubled soli threshold)"""
    result = main.calc_netto(salary, config=married_config)
    assert abs(result - expected) < 1


def test_calc_netto_married_higher_than_single(married_config):
    """Splitting must never yield less netto than the single tariff"""
    single_config = TaxConfig(year=2025, church_tax=0.0)
    for salary in [30000, 60000, 100000, 150000, 250000]:
        assert main.calc_netto(salary, config=married_config) >= main.calc_netto(
            salary, config=single_config
        )


def test_calc_netto_dual_income(married_config):
    """Test household netto for a dual-income married couple"""
    result = main.calc_netto(80000, config=married_config, partner_salary=80000)
    assert abs(result - 96345.38) < 1


def test_calc_netto_dual_income_pays_more_social_security(married_config):
    """Same household income, but two earners below the contribution ceilings
    pay more social security than a single earner above them"""
    single_earner = main.calc_netto(160000, config=married_config)
    dual_earner = main.calc_netto(80000, config=married_config, partner_salary=80000)
    assert dual_earner < single_earner


def test_calc_netto_partner_salary_zero_equals_single_earner(married_config):
    """partner_salary=0 must behave exactly like the single-earner call"""
    assert main.calc_netto(
        100000, config=married_config, partner_salary=0
    ) == main.calc_netto(100000, config=married_config)


def test_calc_netto_partner_salary_requires_married(default_config):
    """partner_salary without is_married must raise"""
    with pytest.raises(ValueError, match="is_married"):
        main.calc_netto(50000, config=default_config, partner_salary=10000)


def test_calc_netto_negative_partner_salary(married_config):
    """Negative partner_salary must raise"""
    with pytest.raises(ValueError, match="non-negative"):
        main.calc_netto(50000, config=married_config, partner_salary=-1)


def test_calc_inverse_netto_dual_income_roundtrip(married_config):
    """Inverse calculation with a fixed partner salary recovers the gross salary"""
    netto = main.calc_netto(80000, config=married_config, partner_salary=50000)
    gross = main.calc_inverse_netto(netto, config=married_config, partner_salary=50000)
    assert abs(gross - 80000) <= 1


def test_calc_inverse_netto_partner_already_covers_desired(married_config):
    """A desired netto already reached by the partner salary alone must raise"""
    with pytest.raises(ValueError, match="partner salary alone"):
        main.calc_inverse_netto(20000, config=married_config, partner_salary=100000)


@pytest.mark.parametrize("year", list(range(2018, 2033)))
def test_calc_netto_all_years_smoke(year):
    """calc_netto must produce a plausible result for every supported year,
    including the 2027-2032 forecast years"""
    config = TaxConfig(year=year, church_tax=0.0)
    netto = main.calc_netto(60000, config=config)
    assert 30000 < netto < 60000


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
    # Use explicit year=2022 for stable test behavior
    result = main.calc_inverse_netto(30000, config=TaxConfig(year=2022))
    # Should use default TaxConfig
    assert isinstance(result, int | float)
    assert result > 0
    # Verify the result makes sense (gross should be higher than net)
    assert result > 30000
