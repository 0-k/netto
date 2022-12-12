import math

from scipy.integrate import quad

import netto.config as config
from netto.const import tax_curve


def get_marginal_tax_rate(taxable_income):
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
    return (1 - (x_j - x) / (x_j - x_i)) * (y_j - y_i) + y_i


def calc_taxable_income(salary, deductible_social_security, deductables_other=0):
    return math.floor(
        max(0, salary - deductible_social_security - 1200 - 36 - deductables_other)
    )


def calc_income_tax(taxable_income):
    taxable_income = round(taxable_income)
    if taxable_income <= tax_curve[config.year][0]["step"]:
        return 0
    elif taxable_income <= tax_curve[config.year][1]["step"]:
        y = (taxable_income - tax_curve[config.year][0]["step"]) / 10000
        return (
            tax_curve[config.year][1]["const"][0] * y
            + tax_curve[config.year][1]["const"][1]
        ) * y
    elif taxable_income <= tax_curve[config.year][2]["step"]:
        z = (taxable_income - tax_curve[config.year][1]["step"]) / 10000
        return (
            tax_curve[config.year][2]["const"][0] * z
            + tax_curve[config.year][2]["const"][1]
        ) * z + tax_curve[config.year][2]["const"][2]
    elif taxable_income <= tax_curve[config.year][3]["step"]:
        return (
            tax_curve[config.year][2]["rate"] * taxable_income
            - tax_curve[config.year][3]["const"][0]
        )
    else:
        return (
            tax_curve[config.year][3]["rate"] * taxable_income
            - tax_curve[config.year][3]["const"][1]
        )


def calc_income_tax_by_integration(taxable_income):
    integral, _ = quad(get_marginal_tax_rate, 0, taxable_income)
    return integral
