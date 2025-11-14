from dataclasses import dataclass


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
