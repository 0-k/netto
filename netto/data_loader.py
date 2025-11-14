"""
Data loader for tax and social security data.

This module loads tax data from JSON files and provides validation
using Pydantic models. It replaces the hardcoded data dictionaries
from const.py with a more maintainable file-based approach.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union

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

    start_taxable_income: float = Field(gt=0, description="Income threshold where soli starts")
    start_fraction: float = Field(ge=0, le=1, description="Starting fraction for progressive phase-in")
    end_rate: float = Field(ge=0, le=1, description="Maximum soli rate")


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


def load_soli() -> Dict[int, dict]:
    """
    Load all solidarity tax data.

    Returns
    -------
    dict
        Soli data for all years

    Examples
    --------
    >>> soli = load_soli()
    >>> soli[2022]['end_rate']
    0.055
    """
    file_path = DATA_DIR / "soli.json"

    if not file_path.exists():
        raise FileNotFoundError("Soli data not found")

    with open(file_path) as f:
        data = json.load(f)

    # Validate each year's data
    validated_data = {}
    for year_str, year_data in data.items():
        year = int(year_str)
        soli_curve = SoliCurve(**year_data)
        validated_data[year] = soli_curve.model_dump()

    return validated_data


def load_pension_correction_factors() -> Dict[int, float]:
    """
    Load pension correction factors.

    Returns
    -------
    dict
        Pension correction factors for all years

    Examples
    --------
    >>> factors = load_pension_correction_factors()
    >>> factors[2022]
    0.88
    """
    file_path = DATA_DIR / "pension_correction_factors.json"

    if not file_path.exists():
        raise FileNotFoundError("Pension correction factors not found")

    with open(file_path) as f:
        data = json.load(f)

    # Convert string keys to integers and validate values
    validated_data = {}
    for year_str, value in data.items():
        year = int(year_str)
        if not isinstance(value, (int, float)):
            raise ValueError(f"Invalid pension correction factor for {year}: {value}")
        if not (0 <= value <= 1):
            raise ValueError(f"Pension correction factor must be between 0 and 1, got {value}")
        validated_data[year] = float(value)

    return validated_data


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
