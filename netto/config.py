from dataclasses import dataclass


@dataclass(slots=True)
class TaxConfig:
    """
    Configuration for tax and social security calculations.

    Parameters
    ----------
    year : int
        Tax year (2018-2032, default: 2025). Years 2018-2025 use enacted
        law, 2026 uses preliminary official data, 2027-2032 are forecasts
        (see data/README.md for assumptions).
    has_children : bool
        Has (or ever had) children - removes the childless surcharge on
        nursing insurance. Automatically set to True if num_children > 0.
    num_children : int
        Number of children entitled to Kindergeld / child allowances.
        When > 0, calc_netto includes Kindergeld in the result and applies
        the Günstigerprüfung (Kindergeld vs. Kinderfreibetrag).
    is_married : bool
        Married status (doubles tax brackets)
    extra_health_insurance : float or None
        Total health insurance Zusatzbeitrag (e.g. 0.029 for 2.9%; the
        employee pays half). Defaults to None, which uses the official
        year-specific average rate from the data files. Set explicitly to
        match your Krankenkasse.
    church_tax : float
        Church tax rate (set to 0.0 for none)

    Examples
    --------
    >>> TaxConfig()
    >>> TaxConfig(year=2025, is_married=True, has_children=True)
    >>> TaxConfig(year=2026, is_married=True, num_children=2)
    >>> TaxConfig(church_tax=0.0)
    >>> TaxConfig(extra_health_insurance=0.019)  # cheap Krankenkasse
    """

    year: int = 2025
    has_children: bool = False
    num_children: int = 0
    is_married: bool = False
    extra_health_insurance: float | None = None
    church_tax: float = 0.09

    def __post_init__(self):
        """Validate configuration values."""
        if not isinstance(self.year, int):
            raise TypeError(f"year must be int, got {type(self.year)}")
        if self.year < 2018 or self.year > 2032:
            raise ValueError(f"year must be between 2018 and 2032, got {self.year}")
        if not isinstance(self.has_children, bool):
            raise TypeError(f"has_children must be bool, got {type(self.has_children)}")
        if not isinstance(self.num_children, int) or isinstance(
            self.num_children, bool
        ):
            raise TypeError(f"num_children must be int, got {type(self.num_children)}")
        if self.num_children < 0:
            raise ValueError(
                f"num_children must be non-negative, got {self.num_children}"
            )
        if self.num_children > 0:
            self.has_children = True
        if not isinstance(self.is_married, bool):
            raise TypeError(f"is_married must be bool, got {type(self.is_married)}")
        if self.extra_health_insurance is not None and self.extra_health_insurance < 0:
            raise ValueError(
                f"extra_health_insurance must be non-negative, got {self.extra_health_insurance}"
            )
        if self.church_tax < 0:
            raise ValueError(f"church_tax must be non-negative, got {self.church_tax}")
