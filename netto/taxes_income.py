import math

from scipy.integrate import quad

from netto.config import TaxConfig
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

    # If the person is married, double the tax brackets
    if config.is_married:
        tax_curve = {
            year: {
                bracket: {
                    "step": data["step"] * 2,
                    "rate": data["rate"],
                    "const": data.get("const", []),
                }
                for bracket, data in year_data.items()
            }
            for year, year_data in TAX_CURVE_DATA.items()
        }
    else:
        tax_curve = TAX_CURVE_DATA
    if taxable_income < tax_curve[config.year][0]["step"]:
        return 0
    elif taxable_income <= tax_curve[config.year][1]["step"]:
        return __calc_gradient(
            tax_curve[config.year][0]["step"],
            tax_curve[config.year][1]["step"],
            tax_curve[config.year][0]["rate"],
            tax_curve[config.year][1]["rate"],
            taxable_income,
        )
    elif taxable_income <= tax_curve[config.year][2]["step"]:
        return __calc_gradient(
            tax_curve[config.year][1]["step"],
            tax_curve[config.year][2]["step"],
            tax_curve[config.year][1]["rate"],
            tax_curve[config.year][2]["rate"],
            taxable_income,
        )
    elif taxable_income < tax_curve[config.year][3]["step"]:
        return tax_curve[config.year][2]["rate"]
    else:
        return tax_curve[config.year][3]["rate"]


def __calc_gradient(x_i: float, x_j: float, y_i: float, y_j: float, x: float) -> float:
    return (1 - (x_j - x) / (x_j - x_i)) * (y_j - y_i) + y_i


def calc_taxable_income(
    salary: float, deductible_social_security: float, deductibles_other: float = 0
) -> float:
    """
    Calculate the taxable income for a given salary and deductibles.

    Parameters
    ----------
    salary: float or int
        The yearly salary for which the taxable income should be calculated.
    deductible_social_security: float or int
        The amount of deductible social security contributions.
    deductibles_other: float or int, optional
        Other deductibles that reduce the taxable income (default is 0).

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

    return math.floor(
        max(0, salary - deductible_social_security - 1200 - 36 - deductibles_other)
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
