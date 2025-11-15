import pytest

from netto.config import TaxConfig


def test_taxconfig_defaults():
    """Test that TaxConfig uses correct default values"""
    config = TaxConfig()
    assert config.year == 2022
    assert config.has_children is False
    assert config.is_married is False
    assert config.extra_health_insurance == 0.014
    assert config.church_tax == 0.09


def test_taxconfig_custom_values():
    """Test creating TaxConfig with custom values"""
    config = TaxConfig(
        year=2025,
        has_children=True,
        is_married=True,
        extra_health_insurance=0.02,
        church_tax=0.08
    )
    assert config.year == 2025
    assert config.has_children is True
    assert config.is_married is True
    assert config.extra_health_insurance == 0.02
    assert config.church_tax == 0.08


def test_taxconfig_validation_year_range():
    """Test that year validation works"""
    with pytest.raises(ValueError):
        TaxConfig(year=2017)  # Too early
    with pytest.raises(ValueError):
        TaxConfig(year=2026)  # Too late


def test_taxconfig_validation_negative_rates():
    """Test that negative rates are rejected"""
    with pytest.raises(ValueError):
        TaxConfig(extra_health_insurance=-0.01)
    with pytest.raises(ValueError):
        TaxConfig(church_tax=-0.01)


def test_taxconfig_validation_type_errors():
    """Test that type validation works"""
    with pytest.raises(TypeError):
        TaxConfig(year="2022")  # String instead of int
    with pytest.raises(TypeError):
        TaxConfig(has_children="True")  # String instead of bool
    with pytest.raises(TypeError):
        TaxConfig(is_married=1)  # Int instead of bool
