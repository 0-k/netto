import pytest
from pydantic import ValidationError

from netto.data_loader import (
    PensionFactor,
    SocialSecurity,
    SocialSecurityEntry,
    SoliCurve,
    TaxBracket,
    TaxCurve,
    correction_factor_pensions,
    load_all_pension_factors,
    load_all_social_security,
    load_all_soli,
    load_all_tax_curves,
    load_pension_factor,
    load_social_security,
    load_soli,
    load_tax_curve,
    social_security_curve,
    soli_curve,
    tax_curve,
)

# Tests for Pydantic Models


def test_tax_bracket_valid():
    """Test creating a valid TaxBracket"""
    bracket = TaxBracket(step=10000, rate=0.14, const=[100, 200])
    assert bracket.step == 10000
    assert bracket.rate == 0.14
    assert bracket.const == [100, 200]


def test_tax_bracket_no_const():
    """Test creating TaxBracket without const"""
    bracket = TaxBracket(step=10000, rate=0.0)
    assert bracket.step == 10000
    assert bracket.rate == 0.0
    assert bracket.const is None


def test_tax_bracket_invalid_step():
    """Test that TaxBracket rejects invalid step values"""
    with pytest.raises(ValidationError):
        TaxBracket(step=0, rate=0.14)  # step must be > 0
    with pytest.raises(ValidationError):
        TaxBracket(step=-100, rate=0.14)  # negative not allowed


def test_tax_bracket_invalid_rate():
    """Test that TaxBracket rejects invalid rate values"""
    with pytest.raises(ValidationError):
        TaxBracket(step=10000, rate=-0.1)  # negative not allowed
    with pytest.raises(ValidationError):
        TaxBracket(step=10000, rate=1.5)  # > 1 not allowed


def test_tax_bracket_empty_const():
    """Test that TaxBracket rejects empty const array"""
    with pytest.raises(ValidationError):
        TaxBracket(step=10000, rate=0.14, const=[])


def test_tax_curve_valid():
    """Test creating a valid TaxCurve"""
    curve = TaxCurve(
        year=2022,
        brackets={
            "0": TaxBracket(step=10347, rate=0.0),
            "1": TaxBracket(step=14927, rate=0.14, const=[995.21, 1400]),
            "2": TaxBracket(step=58597, rate=0.2397, const=[208.85, 2397, 950.96]),
            "3": TaxBracket(step=277826, rate=0.42, const=[0.42, 9336.45]),
        },
    )
    assert curve.year == 2022
    assert len(curve.brackets) == 4


def test_tax_curve_invalid_brackets():
    """Test that TaxCurve requires exactly 4 brackets"""
    with pytest.raises(ValidationError):
        TaxCurve(
            year=2022,
            brackets={
                "0": TaxBracket(step=10000, rate=0.0),
                "1": TaxBracket(step=20000, rate=0.14),
            },
        )


def test_tax_curve_invalid_year():
    """Test that TaxCurve validates year range"""
    with pytest.raises(ValidationError):
        TaxCurve(
            year=2015,  # Too early
            brackets={
                "0": TaxBracket(step=10000, rate=0.0),
                "1": TaxBracket(step=20000, rate=0.14),
                "2": TaxBracket(step=30000, rate=0.24),
                "3": TaxBracket(step=40000, rate=0.42),
            },
        )


def test_social_security_entry_valid():
    """Test creating a valid SocialSecurityEntry"""
    entry = SocialSecurityEntry(limit=84600, rate=0.093)
    assert entry.limit == 84600
    assert entry.rate == 0.093
    assert entry.extra is None


def test_social_security_entry_with_extra():
    """Test creating SocialSecurityEntry with extra rate"""
    entry = SocialSecurityEntry(limit=58050, rate=0.073, extra=0.0035)
    assert entry.limit == 58050
    assert entry.rate == 0.073
    assert entry.extra == 0.0035


def test_social_security_entry_invalid_limit():
    """Test that SocialSecurityEntry validates limit"""
    with pytest.raises(ValidationError):
        SocialSecurityEntry(limit=0, rate=0.093)  # Must be > 0
    with pytest.raises(ValidationError):
        SocialSecurityEntry(limit=-1000, rate=0.093)  # Negative not allowed


def test_social_security_valid():
    """Test creating a valid SocialSecurity"""
    ss = SocialSecurity(
        year=2022,
        pension=SocialSecurityEntry(limit=84600, rate=0.093),
        unemployment=SocialSecurityEntry(limit=84600, rate=0.012),
        health=SocialSecurityEntry(limit=58050, rate=0.073, extra=0.007),
        nursing=SocialSecurityEntry(limit=58050, rate=0.01525, extra=0.0035),
    )
    assert ss.year == 2022
    assert ss.pension.limit == 84600
    assert ss.health.extra == 0.007


def test_soli_curve_valid():
    """Test creating a valid SoliCurve"""
    soli = SoliCurve(
        year=2022, start_taxable_income=16956, start_fraction=0.119, end_rate=0.055
    )
    assert soli.year == 2022
    assert soli.start_taxable_income == 16956
    assert soli.start_fraction == 0.119
    assert soli.end_rate == 0.055


def test_pension_factor_valid():
    """Test creating a valid PensionFactor"""
    factor = PensionFactor(year=2022, factor=0.88)
    assert factor.year == 2022
    assert factor.factor == 0.88


def test_pension_factor_invalid_factor():
    """Test that PensionFactor validates factor range"""
    with pytest.raises(ValidationError):
        PensionFactor(year=2022, factor=-0.1)  # Negative not allowed
    with pytest.raises(ValidationError):
        PensionFactor(year=2022, factor=1.5)  # > 1 not allowed


# Tests for individual load functions


@pytest.mark.parametrize("year", [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
def test_load_tax_curve(year):
    """Test loading tax curve for available years"""
    curve = load_tax_curve(year)
    assert isinstance(curve, dict)
    assert len(curve) == 4
    assert all(k in [0, 1, 2, 3] for k in curve.keys())
    assert all("step" in v and "rate" in v for v in curve.values())


def test_load_tax_curve_missing_year():
    """Test that loading tax curve for missing year raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        load_tax_curve(2030)


@pytest.mark.parametrize("year", [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
def test_load_social_security(year):
    """Test loading social security for available years"""
    ss = load_social_security(year)
    assert isinstance(ss, dict)
    assert "pension" in ss
    assert "unemployment" in ss
    assert "health" in ss
    assert "nursing" in ss


def test_load_social_security_not_implemented():
    """Test that loading social security for 2026+ raises NotImplementedError"""
    with pytest.raises(NotImplementedError):
        load_social_security(2026)


def test_load_social_security_missing_year():
    """Test that loading social security for missing year raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        load_social_security(2015)


@pytest.mark.parametrize("year", [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
def test_load_soli(year):
    """Test loading solidarity tax data for available years"""
    soli = load_soli(year)
    assert isinstance(soli, dict)
    assert "start_taxable_income" in soli
    assert "start_fraction" in soli
    assert "end_rate" in soli


def test_load_soli_missing_year():
    """Test that loading soli for missing year raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        load_soli(2030)


@pytest.mark.parametrize("year", [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
def test_load_pension_factor(year):
    """Test loading pension factor for available years"""
    factor = load_pension_factor(year)
    assert isinstance(factor, float)
    assert 0 <= factor <= 1


def test_load_pension_factor_missing_year():
    """Test that loading pension factor for missing year raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        load_pension_factor(2030)


# Tests for bulk load functions


def test_load_all_tax_curves():
    """Test loading all tax curves"""
    curves = load_all_tax_curves()
    assert isinstance(curves, dict)
    assert len(curves) >= 8  # At least 2018-2025
    for year, curve in curves.items():
        assert isinstance(year, int)
        assert isinstance(curve, dict)
        assert len(curve) == 4


def test_load_all_social_security():
    """Test loading all social security data"""
    ss_data = load_all_social_security()
    assert isinstance(ss_data, dict)
    assert len(ss_data) >= 8  # At least 2018-2025
    # Check for 2026 NotImplementedError marker
    assert 2026 in ss_data
    assert ss_data[2026] is NotImplementedError


def test_load_all_soli():
    """Test loading all solidarity tax data"""
    soli_data = load_all_soli()
    assert isinstance(soli_data, dict)
    assert len(soli_data) >= 8  # At least 2018-2025
    for year, soli in soli_data.items():
        assert isinstance(year, int)
        assert isinstance(soli, dict)


def test_load_all_pension_factors():
    """Test loading all pension factors"""
    factors = load_all_pension_factors()
    assert isinstance(factors, dict)
    assert len(factors) >= 8  # At least 2018-2025
    for year, factor in factors.items():
        assert isinstance(year, int)
        assert isinstance(factor, float)
        assert 0 <= factor <= 1


# Tests for module-level variables


def test_module_tax_curve():
    """Test that tax_curve is loaded at module level"""
    assert isinstance(tax_curve, dict)
    assert len(tax_curve) >= 8
    assert 2022 in tax_curve
    assert len(tax_curve[2022]) == 4


def test_module_social_security_curve():
    """Test that social_security_curve is loaded at module level"""
    assert isinstance(social_security_curve, dict)
    assert len(social_security_curve) >= 8
    assert 2022 in social_security_curve
    assert "pension" in social_security_curve[2022]


def test_module_soli_curve():
    """Test that soli_curve is loaded at module level"""
    assert isinstance(soli_curve, dict)
    assert len(soli_curve) >= 8
    assert 2022 in soli_curve
    assert "start_taxable_income" in soli_curve[2022]


def test_module_correction_factor_pensions():
    """Test that correction_factor_pensions is loaded at module level"""
    assert isinstance(correction_factor_pensions, dict)
    assert len(correction_factor_pensions) >= 8
    assert 2022 in correction_factor_pensions
    assert isinstance(correction_factor_pensions[2022], float)


# Integration tests


def test_tax_curve_structure_2022():
    """Test that 2022 tax curve has expected structure"""
    curve_2022 = load_tax_curve(2022)

    # Bracket 0: Basic allowance
    assert curve_2022[0]["step"] == 10347
    assert curve_2022[0]["rate"] == 0.14

    # Bracket 1: Progressive zone 1
    assert curve_2022[1]["step"] == 14926
    assert curve_2022[1]["rate"] == 0.2397
    assert curve_2022[1]["const"] is not None

    # Bracket 2: Progressive zone 2
    assert curve_2022[2]["step"] == 58596
    assert curve_2022[2]["rate"] == 0.42
    assert curve_2022[2]["const"] is not None

    # Bracket 3: Top rate
    assert curve_2022[3]["step"] == 277826
    assert curve_2022[3]["rate"] == 0.45


def test_social_security_structure_2022():
    """Test that 2022 social security has expected structure"""
    ss_2022 = load_social_security(2022)

    # Pension insurance
    assert ss_2022["pension"]["limit"] == 84600
    assert ss_2022["pension"]["rate"] == 0.093

    # Health insurance
    assert ss_2022["health"]["limit"] == 58050
    assert ss_2022["health"]["rate"] == 0.073

    # Nursing insurance
    assert ss_2022["nursing"]["limit"] == 58050
    assert ss_2022["nursing"]["rate"] == 0.01525


def test_soli_structure_2022():
    """Test that 2022 soli has expected structure"""
    soli_2022 = load_soli(2022)

    assert soli_2022["start_taxable_income"] == 16956
    assert soli_2022["start_fraction"] == 0.119
    assert soli_2022["end_rate"] == 0.055


def test_pension_factor_value_2022():
    """Test that 2022 pension factor has expected value"""
    factor_2022 = load_pension_factor(2022)

    assert factor_2022 == 0.88
