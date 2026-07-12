import math
from dataclasses import replace

from scipy.integrate import quad

from netto.config import TaxConfig
from netto.data_loader import deductions as DEDUCTIONS_DATA
from netto.data_loader import tax_curve as TAX_CURVE_DATA


def get_marginal_tax_rate(
    taxable_income: float, config: TaxConfig | None = None
) -> float:
    """
    Calculate the marginal tax rate for a given taxable income.

    Parameters
    ----------
    taxable_income: float or int
        The taxable income for which the marginal tax rate should be calculated.
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    marginal_tax_rate: float
        The marginal tax rate for the given taxable income.

    Examples
    --------
    # Calculate marginal tax rate for a taxable income of 10000
    get_marginal_tax_rate(10000)
    """
    if config is None:
        config = TaxConfig()

    # Married couples (Ehegattensplitting): stretching the bracket boundaries
    # by 2 makes the marginal rate curve equivalent to 2 * tax(income / 2)
    splitting_factor = 2 if config.is_married else 1
    tax_curve = {
        bracket: {
            "step": data["step"] * splitting_factor,
            "rate": data["rate"],
        }
        for bracket, data in TAX_CURVE_DATA[config.year].items()
    }
    if taxable_income < tax_curve[0]["step"]:
        return 0
    elif taxable_income <= tax_curve[1]["step"]:
        return __calc_gradient(
            tax_curve[0]["step"],
            tax_curve[1]["step"],
            tax_curve[0]["rate"],
            tax_curve[1]["rate"],
            taxable_income,
        )
    elif taxable_income <= tax_curve[2]["step"]:
        return __calc_gradient(
            tax_curve[1]["step"],
            tax_curve[2]["step"],
            tax_curve[1]["rate"],
            tax_curve[2]["rate"],
            taxable_income,
        )
    elif taxable_income < tax_curve[3]["step"]:
        return tax_curve[2]["rate"]
    else:
        return tax_curve[3]["rate"]


def __calc_gradient(x_i: float, x_j: float, y_i: float, y_j: float, x: float) -> float:
    return (1 - (x_j - x) / (x_j - x_i)) * (y_j - y_i) + y_i


def calc_taxable_income(
    salary: float,
    deductible_social_security: float,
    deductibles_other: float = 0,
    config: TaxConfig | None = None,
    partner_salary: float = 0,
) -> float:
    """
    Calculate the taxable income for a given salary and deductibles.

    Applies the year-specific employee lump-sum deduction
    (Arbeitnehmer-Pauschbetrag) per earner and the special expenses lump sum
    (Sonderausgaben-Pauschbetrag), which doubles for married couples under
    joint assessment.

    Parameters
    ----------
    salary: float or int
        The yearly salary for which the taxable income should be calculated.
    deductible_social_security: float or int
        The amount of deductible social security contributions
        (for both partners combined if partner_salary is given).
    deductibles_other: float or int, optional
        Other deductibles that reduce the taxable income (default is 0).
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)
    partner_salary: float or int, optional
        Yearly salary of the spouse for jointly assessed couples (default is 0).

    Returns
    -------
    taxable_income: float
        The taxable income for the given salary and deductibles.

    Examples
    --------
    # Calculate taxable income for a salary of 50000 with deductible social security contributions of 1000 and no other deductibles
    calc_taxable_income(50000, 1000)

    # Calculate taxable income for a salary of 60000 with deductible social security contributions of 2000 and other deductibles of 500
    calc_taxable_income(60000, 2000, 500)
    """
    if config is None:
        config = TaxConfig()

    werbungskosten = DEDUCTIONS_DATA[config.year]["werbungskosten_pauschbetrag"]
    sonderausgaben = DEDUCTIONS_DATA[config.year]["sonderausgaben_pauschbetrag"] * (
        2 if config.is_married else 1
    )
    income = max(0, salary - werbungskosten)
    if partner_salary > 0:
        income += max(0, partner_salary - werbungskosten)
    return math.floor(
        max(
            0,
            income - deductible_social_security - sonderausgaben - deductibles_other,
        )
    )


def calc_income_tax(taxable_income: float, config: TaxConfig | None = None) -> float:
    """
    Calculate the income tax for a given taxable income.

    Parameters
    ----------
    taxable_income: float or int
        The taxable income for which the income tax should be calculated.
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    income_tax: float
        The income tax for the given taxable income.

    Examples
    --------
    # Calculate income tax for a taxable income of 10000
    calc_income_tax(10000)
    """
    if config is None:
        config = TaxConfig()

    # Ehegattensplitting: tax the halved income at the single tariff, doubled
    if config.is_married:
        return 2 * calc_income_tax(
            taxable_income / 2, replace(config, is_married=False)
        )

    taxable_income = round(taxable_income)
    if taxable_income <= TAX_CURVE_DATA[config.year][0]["step"]:
        return 0
    elif taxable_income <= TAX_CURVE_DATA[config.year][1]["step"]:
        y = (taxable_income - TAX_CURVE_DATA[config.year][0]["step"]) / 10000
        return (
            TAX_CURVE_DATA[config.year][1]["const"][0] * y
            + TAX_CURVE_DATA[config.year][1]["const"][1]
        ) * y
    elif taxable_income <= TAX_CURVE_DATA[config.year][2]["step"]:
        z = (taxable_income - TAX_CURVE_DATA[config.year][1]["step"]) / 10000
        return (
            TAX_CURVE_DATA[config.year][2]["const"][0] * z
            + TAX_CURVE_DATA[config.year][2]["const"][1]
        ) * z + TAX_CURVE_DATA[config.year][2]["const"][2]
    elif taxable_income <= TAX_CURVE_DATA[config.year][3]["step"]:
        return (
            TAX_CURVE_DATA[config.year][2]["rate"] * taxable_income
            - TAX_CURVE_DATA[config.year][3]["const"][0]
        )
    else:
        return (
            TAX_CURVE_DATA[config.year][3]["rate"] * taxable_income
            - TAX_CURVE_DATA[config.year][3]["const"][1]
        )


def calc_income_tax_by_integration(
    taxable_income: float, config: TaxConfig | None = None
) -> float:
    """
    Calculate income tax by numerical integration of marginal tax rates.

    Parameters
    ----------
    taxable_income: float
        Taxable income
    config : TaxConfig, optional
        Tax configuration (uses defaults if not provided)

    Returns
    -------
    float
        Income tax amount

    Examples
    --------
    >>> calc_income_tax_by_integration(10000)
    """
    if config is None:
        config = TaxConfig()

    income_tax, _ = quad(
        lambda ti: get_marginal_tax_rate(ti, config), 0, taxable_income
    )
    return income_tax
