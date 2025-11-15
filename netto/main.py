from scipy.optimize import newton

from netto.config import TaxConfig
from netto.social_security import calc_deductible_social_security, calc_social_security
from netto.taxes_income import calc_income_tax_by_integration, calc_taxable_income
from netto.taxes_other import calc_church_tax, calc_soli


def calc_netto(
    salary: float,
    deductibles: float = 0,
    verbose: bool = False,
    config: TaxConfig | None = None,
) -> float:
    """
    Calculate net income from gross salary.

    Parameters
    ----------
    salary: float
        Yearly gross salary
    deductibles: float, optional
        Additional deductibles that reduce taxable income
    verbose: bool, optional
        Print detailed calculation breakdown
    config : TaxConfig, optional
        Tax configuration (uses defaults if not provided)

    Returns
    -------
    float
        Net income

    Examples
    --------
    >>> calc_netto(50000)
    >>> calc_netto(50000, deductibles=10000)
    >>> calc_netto(50000, verbose=True)
    >>> config = TaxConfig(year=2025, is_married=True)
    >>> calc_netto(50000, config=config)
    """
    if config is None:
        config = TaxConfig()

    deductible_social_security = calc_deductible_social_security(salary, config)
    taxable_income = calc_taxable_income(
        salary=salary,
        deductible_social_security=deductible_social_security,
        deductibles_other=deductibles,
    )
    income_tax = calc_income_tax_by_integration(taxable_income, config)
    if verbose:
        repr = (
            "Yearly Evaluation:\n"
            + f"Income Tax:      {round(income_tax, 2):>12}\n"
            + f"Soli:            {round(calc_soli(income_tax, config), 2):>12}\n"
            + f"Church Tax:      {round(calc_church_tax(income_tax, config), 2):>12}\n"
            + f"Social Security: {round(calc_social_security(salary, config), 2):>12}"
        )
        print(repr)
    return round(
        (
            salary
            - income_tax
            - calc_soli(income_tax, config)
            - calc_church_tax(income_tax, config)
            - calc_social_security(salary, config)
        ),
        2,
    )


def calc_inverse_netto(
    desired_netto: float, deductibles: float = 0, config: TaxConfig | None = None
) -> float:
    """
    Calculate required gross salary to reach desired net income.

    Parameters
    ----------
    desired_netto: float
        Desired net income
    deductibles: float, optional
        Additional deductibles that reduce taxable income
    config : TaxConfig, optional
        Tax configuration (uses defaults if not provided)

    Returns
    -------
    float
        Required gross salary

    Examples
    --------
    >>> calc_inverse_netto(50000)
    >>> calc_inverse_netto(50000, deductibles=5000)
    >>> config = TaxConfig(year=2025, is_married=True)
    >>> calc_inverse_netto(50000, config=config)
    """
    if config is None:
        config = TaxConfig()

    def f(salary):
        return (
            calc_netto(salary, deductibles=deductibles, config=config) - desired_netto
        )

    return round(newton(f, x0=desired_netto), 0)
