from dataclasses import dataclass


@dataclass(slots=True)
class TaxConfig:
    """
    Configuration for tax and social security calculations.

    Parameters
    ----------
    year : int
        Tax year (2018-2025, default: 2025)
    has_children : bool
        Has children (affects nursing insurance)
    is_married : bool
        Married status (doubles tax brackets)
    extra_health_insurance : float
        Extra health insurance rate
    church_tax : float
        Church tax rate (set to 0.0 for none)

    Examples
    --------
    >>> TaxConfig()
    >>> TaxConfig(year=2025, is_married=True, has_children=True)
    >>> TaxConfig(church_tax=0.0)
    """

    year: int = 2025
    has_children: bool = False
    is_married: bool = False
    extra_health_insurance: float = 0.025
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
            raise ValueError(
                f"extra_health_insurance must be non-negative, got {self.extra_health_insurance}"
            )
        if self.church_tax < 0:
            raise ValueError(f"church_tax must be non-negative, got {self.church_tax}")
