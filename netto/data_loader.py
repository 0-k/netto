"""
Data loader for tax and social security data.

This module loads tax data from JSON files and provides validation
using Pydantic models. All data is organized in individual yearly files
for better maintainability and auditability.

The loaded data is exposed as module-level variables for easy import:
- tax_curve: Tax brackets by year
- social_security_curve: Social security rates by year
- soli_curve: Solidarity tax parameters by year
- correction_factor_pensions: Pension deduction factors by year
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# Get the data directory path
DATA_DIR = Path(__file__).parent.parent / "data"


class TaxBracket(BaseModel):
    """Tax bracket configuration for a single bracket."""

    step: float = Field(gt=0, description="Income threshold for this bracket")
    rate: float = Field(ge=0, le=1, description="Tax rate for this bracket")
    const: Optional[List[float]] = Field(default=None, description="Polynomial coefficients")

    @field_validator("const")
    @classmethod
    def validate_const_length(cls, v, info):
        """Validate that const array has correct length based on bracket."""
        if v is not None and len(v) == 0:
            raise ValueError("const array cannot be empty")
        return v


class TaxCurve(BaseModel):
    """Tax curve configuration for a single year."""

    year: int = Field(ge=2018, le=2030, description="Tax year")
    brackets: Dict[str, TaxBracket] = Field(description="Tax brackets (0-3)")

    @field_validator("brackets")
    @classmethod
    def validate_brackets(cls, v):
        """Ensure we have exactly 4 brackets (0-3)."""
        if set(v.keys()) != {"0", "1", "2", "3"}:
            raise ValueError("Tax curve must have exactly 4 brackets (0-3)")
        return v


class SocialSecurityEntry(BaseModel):
    """Social security entry for pension, unemployment, health, or nursing."""

    limit: float = Field(gt=0, description="Income limit for this contribution")
    rate: float = Field(ge=0, le=1, description="Contribution rate")
    extra: Optional[float] = Field(default=None, ge=0, le=1, description="Extra rate (nursing only)")


class SocialSecurity(BaseModel):
    """Social security configuration for a single year."""

    year: int = Field(ge=2018, le=2030, description="Tax year")
    pension: SocialSecurityEntry
    unemployment: SocialSecurityEntry
    health: SocialSecurityEntry
    nursing: SocialSecurityEntry


class SoliCurve(BaseModel):
    """Solidarity tax configuration for a single year."""

    year: int = Field(ge=2018, le=2030, description="Tax year")
    start_taxable_income: float = Field(gt=0, description="Income threshold where soli starts")
    start_fraction: float = Field(ge=0, le=1, description="Starting fraction for progressive phase-in")
    end_rate: float = Field(ge=0, le=1, description="Maximum soli rate")


class PensionFactor(BaseModel):
    """Pension correction factor for a single year."""

    year: int = Field(ge=2018, le=2030, description="Tax year")
    factor: float = Field(ge=0, le=1, description="Pension deduction factor")


def load_tax_curve(year: int) -> Dict[int, dict]:
    """
    Load tax curve for a specific year.

    Parameters
    ----------
    year : int
        Tax year to load

    Returns
    -------
    dict
        Tax curve data as dictionary with integer keys (0-3)

    Examples
    --------
    >>> curve = load_tax_curve(2022)
    >>> curve[0]['step']
    10347
    """
    file_path = DATA_DIR / "tax_curves" / f"{year}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Tax curve data not found for year {year}")

    with open(file_path) as f:
        data = json.load(f)

    # Validate with pydantic
    tax_curve = TaxCurve(**data)

    # Convert string keys to integers for backward compatibility
    return {int(k): v.model_dump() for k, v in tax_curve.brackets.items()}


def load_social_security(year: int) -> dict:
    """
    Load social security data for a specific year.

    Parameters
    ----------
    year : int
        Tax year to load

    Returns
    -------
    dict
        Social security data

    Examples
    --------
    >>> ss = load_social_security(2022)
    >>> ss['pension']['limit']
    84600
    """
    file_path = DATA_DIR / "social_security" / f"{year}.json"

    if not file_path.exists():
        if year >= 2026:
            raise NotImplementedError(f"Social security data not yet available for {year}")
        raise FileNotFoundError(f"Social security data not found for year {year}")

    with open(file_path) as f:
        data = json.load(f)

    # Validate with pydantic
    social_security = SocialSecurity(**data)

    return social_security.model_dump(exclude={"year"})


def load_soli(year: int) -> dict:
    """
    Load solidarity tax data for a specific year.

    Parameters
    ----------
    year : int
        Tax year to load

    Returns
    -------
    dict
        Soli data

    Examples
    --------
    >>> soli = load_soli(2022)
    >>> soli['end_rate']
    0.055
    """
    file_path = DATA_DIR / "soli" / f"{year}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Soli data not found for year {year}")

    with open(file_path) as f:
        data = json.load(f)

    # Validate with pydantic
    soli_curve = SoliCurve(**data)

    return soli_curve.model_dump(exclude={"year"})


def load_pension_factor(year: int) -> float:
    """
    Load pension correction factor for a specific year.

    Parameters
    ----------
    year : int
        Tax year to load

    Returns
    -------
    float
        Pension correction factor

    Examples
    --------
    >>> factor = load_pension_factor(2022)
    >>> factor
    0.88
    """
    file_path = DATA_DIR / "pension_factors" / f"{year}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Pension factor not found for year {year}")

    with open(file_path) as f:
        data = json.load(f)

    # Validate with pydantic
    pension_factor = PensionFactor(**data)

    return pension_factor.factor


def load_all_tax_curves() -> Dict[int, Dict[int, dict]]:
    """
    Load tax curves for all available years.

    Returns
    -------
    dict
        Tax curves for all years
    """
    tax_curves = {}
    for year in range(2018, 2026):  # 2018-2025
        try:
            tax_curves[year] = load_tax_curve(year)
        except FileNotFoundError:
            pass  # Skip missing years
    return tax_curves


def load_all_social_security() -> Dict[int, dict]:
    """
    Load social security data for all available years.

    Returns
    -------
    dict
        Social security data for all years
    """
    social_security = {}
    for year in range(2018, 2026):  # 2018-2025
        try:
            social_security[year] = load_social_security(year)
        except (FileNotFoundError, NotImplementedError):
            pass  # Skip missing years

    # Add NotImplementedError for 2026+ to maintain backward compatibility
    social_security[2026] = NotImplementedError

    return social_security


def load_all_soli() -> Dict[int, dict]:
    """
    Load solidarity tax data for all available years.

    Returns
    -------
    dict
        Soli data for all years
    """
    soli_data = {}
    for year in range(2018, 2026):  # 2018-2025
        try:
            soli_data[year] = load_soli(year)
        except FileNotFoundError:
            pass  # Skip missing years
    return soli_data


def load_all_pension_factors() -> Dict[int, float]:
    """
    Load pension correction factors for all available years.

    Returns
    -------
    dict
        Pension correction factors for all years
    """
    pension_factors = {}
    for year in range(2018, 2026):  # 2018-2025
        try:
            pension_factors[year] = load_pension_factor(year)
        except FileNotFoundError:
            pass  # Skip missing years
    return pension_factors


# Load all data at module import time and expose as module-level variables
# These match the old const.py variable names for backward compatibility
tax_curve = load_all_tax_curves()
social_security_curve = load_all_social_security()
soli_curve = load_all_soli()
correction_factor_pensions = load_all_pension_factors()


# Expose private names for backward compatibility with existing code
# that imports from const.py with leading underscores
__tax_curve = tax_curve
__social_security_curve = social_security_curve
__soli_curve = soli_curve
__correction_factor_pensions = correction_factor_pensions
