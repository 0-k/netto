import math

from scipy.integrate import quad

import netto.config as config
from netto.const import __tax_curve


def get_marginal_tax_rate(taxable_income):
    """
    Calculate the marginal tax rate for a given taxable income.

    Parameters
    ----------
    taxable_income: float or int
        The taxable income for which the marginal tax rate should be calculated.
    is_married: bool
        Whether the person is married or not. If true, the tax brackets are doubled.

    Returns
    -------
    marginal_tax_rate: float
        The marginal tax rate for the given taxable income.

    Examples
    --------
    # Calculate marginal tax rate for a taxable income of 10000
    get_marginal_tax_rate(10000)
    """
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
            for year, year_data in __tax_curve.items()
        }
    else:
        tax_curve = __tax_curve
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


def __calc_gradient(x_i, x_j, y_i, y_j, x):
    # Calculate the gradient between the two points (x_i, y_i) and (x_j, y_j)
    return (1 - (x_j - x) / (x_j - x_i)) * (y_j - y_i) + y_i


def calc_taxable_income(salary, deductible_social_security, deductibles_other=0):
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


def calc_income_tax(taxable_income):
    """
    Calculate the income tax for a given taxable income.

    Parameters
    ----------
    taxable_income: float or int
        The taxable income for which the income tax should be calculated.

    Returns
    -------
    income_tax: float
        The income tax for the given taxable income.

    Examples
    --------
    # Calculate income tax for a taxable income of 10000
    calc_income_tax(10000)
    """

    taxable_income = round(taxable_income)
    if taxable_income <= __tax_curve[config.year][0]["step"]:
        return 0
    elif taxable_income <= __tax_curve[config.year][1]["step"]:
        y = (taxable_income - __tax_curve[config.year][0]["step"]) / 10000
        return (
            __tax_curve[config.year][1]["const"][0] * y
            + __tax_curve[config.year][1]["const"][1]
        ) * y
    elif taxable_income <= __tax_curve[config.year][2]["step"]:
        z = (taxable_income - __tax_curve[config.year][1]["step"]) / 10000
        return (
            __tax_curve[config.year][2]["const"][0] * z
            + __tax_curve[config.year][2]["const"][1]
        ) * z + __tax_curve[config.year][2]["const"][2]
    elif taxable_income <= __tax_curve[config.year][3]["step"]:
        return (
            __tax_curve[config.year][2]["rate"] * taxable_income
            - __tax_curve[config.year][3]["const"][0]
        )
    else:
        return (
            __tax_curve[config.year][3]["rate"] * taxable_income
            - __tax_curve[config.year][3]["const"][1]
        )


def calc_income_tax_by_integration(taxable_income):
    """
    Calculate the income tax for a given taxable income by means of integration.
    Always available, even when exact integration curve in const.py is not defined.

    Parameters
    ----------
    taxable_income: float or int
        The taxable income for which the income tax should be calculated.

    Returns
    -------
    income_tax: float
        The income tax for the given taxable income.

    Examples
    --------
    # Calculate income tax for a taxable income of 10000
    calc_income_tax_by_integration(10000)
    """

    income_tax, _ = quad(get_marginal_tax_rate, 0, taxable_income)
    return income_tax
