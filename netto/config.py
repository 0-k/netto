import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class TaxConfig:
    """
    Configuration for tax and social security calculations.

    Parameters
    ----------
    year : int
        Tax year for calculations (default: 2022)
    has_children : bool
        Whether the taxpayer has children (affects nursing insurance, default: False)
    is_married : bool
        Whether the taxpayer is married (doubles tax brackets, default: False)
    extra_health_insurance : float
        Extra health insurance rate (default: 0.014)
    church_tax : float
        Church tax rate (default: 0.09)

    Examples
    --------
    # Default configuration
    config = TaxConfig()

    # Custom configuration for 2025
    config = TaxConfig(year=2025, is_married=True, has_children=True)

    # No church tax
    config = TaxConfig(church_tax=0.0)
    """

    year: int = 2022
    has_children: bool = False
    is_married: bool = False
    extra_health_insurance: float = 0.014
    church_tax: float = 0.09

    def __post_init__(self):
        """Validate configuration values."""
        if not isinstance(self.year, int):
            raise TypeError(f"year must be int, got {type(self.year)}")
        if self.year < 2018 or self.year > 2025:
            raise ValueError(f"year must be between 2018 and 2025, got {self.year}")
        if not isinstance(self.has_children, bool):
            raise TypeError(f"has_children must be bool, got {type(self.has_children)}")
        if not isinstance(self.is_married, bool):
            raise TypeError(f"is_married must be bool, got {type(self.is_married)}")
        if self.extra_health_insurance < 0:
            raise ValueError(f"extra_health_insurance must be non-negative, got {self.extra_health_insurance}")
        if self.church_tax < 0:
            raise ValueError(f"church_tax must be non-negative, got {self.church_tax}")


def _str_to_bool(s: str) -> bool:
    """Convert string to boolean."""
    if s == "True":
        return True
    elif s == "False":
        return False
    else:
        raise ValueError(f"Invalid boolean string: {s}")


def load_config_from_env() -> TaxConfig:
    """
    Load configuration from environment variables.

    Environment variables:
    - YEAR: Tax year (default: 2022)
    - HAS_CHILDREN: Whether taxpayer has children (default: False)
    - IS_MARRIED: Whether taxpayer is married (default: False)
    - EXTRA_HEALTH_INSURANCE: Extra health insurance rate (default: 0.014)
    - CHURCH_TAX: Church tax rate (default: 0.09)

    Returns
    -------
    TaxConfig
        Configuration loaded from environment variables with fallback to defaults.

    Examples
    --------
    # Load from environment
    config = load_config_from_env()

    # Override specific values
    config = TaxConfig(**{**load_config_from_env().__dict__, 'year': 2025})
    """
    try:
        year = int(os.getenv("YEAR", "2022"))
    except ValueError:
        year = 2022

    try:
        has_children = _str_to_bool(os.getenv("HAS_CHILDREN", "False"))
    except ValueError:
        has_children = False

    try:
        is_married = _str_to_bool(os.getenv("IS_MARRIED", "False"))
    except ValueError:
        is_married = False

    try:
        extra_health_insurance = float(os.getenv("EXTRA_HEALTH_INSURANCE", "0.014"))
    except ValueError:
        extra_health_insurance = 0.014

    try:
        church_tax = float(os.getenv("CHURCH_TAX", "0.09"))
    except ValueError:
        church_tax = 0.09

    return TaxConfig(
        year=year,
        has_children=has_children,
        is_married=is_married,
        extra_health_insurance=extra_health_insurance,
        church_tax=church_tax,
    )


# Default global config for backward compatibility
# Users can either pass TaxConfig to functions or rely on this default
_default_config: Optional[TaxConfig] = None


def get_default_config() -> TaxConfig:
    """
    Get the default global configuration.

    The default config is lazily loaded from environment variables on first access.
    This provides backward compatibility with the old global config approach.

    Returns
    -------
    TaxConfig
        The default configuration instance.
    """
    global _default_config
    if _default_config is None:
        _default_config = load_config_from_env()
    return _default_config


def set_default_config(config: TaxConfig) -> None:
    """
    Set the default global configuration.

    Parameters
    ----------
    config : TaxConfig
        The configuration to set as default.
    """
    global _default_config
    _default_config = config


def reset_default_config() -> None:
    """
    Reset the default configuration to reload from environment variables.

    Useful for testing or when environment variables change.
    """
    global _default_config
    _default_config = None


# Legacy compatibility - these will be deprecated
# Users should migrate to TaxConfig objects
year: int = 0
has_children: bool = False
is_married: bool = False
extra_health_insurance: float = 0.0
church_tax: float = 0.0


def load_config():
    """
    DEPRECATED: Load configuration into global variables.

    This function is maintained for backward compatibility but should not be used
    in new code. Use TaxConfig or load_config_from_env() instead.

    Migration guide:
    - Old: import netto.config as config; config.load_config(); year = config.year
    - New: from netto.config import TaxConfig; config = TaxConfig(); year = config.year
    """
    global year, has_children, is_married, extra_health_insurance, church_tax

    cfg = load_config_from_env()
    year = cfg.year
    has_children = cfg.has_children
    is_married = cfg.is_married
    extra_health_insurance = cfg.extra_health_insurance
    church_tax = cfg.church_tax


# Auto-load for backward compatibility
load_config()
