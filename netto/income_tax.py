import math
from const import *
from config import YEAR


def get_marginal_tax_rate(taxable_income):
    if taxable_income < tax_curve[YEAR][0]["step"]:
        return 0
    elif taxable_income <= tax_curve[YEAR][1]["step"]:
        return __calc_gradient(
            tax_curve[year][0]["step"],
            tax_curve[year][1]["step"],
            tax_curve[year][0]["rate"],
            tax_curve[year][1]["rate"],
            taxable_income,
        )
    elif taxable_income <= tax_curve[YEAR][2]["step"]:
        return __calc_gradient(
            tax_curve[year][1]["step"],
            tax_curve[year][2]["step"],
            tax_curve[year][1]["rate"],
            tax_curve[year][2]["rate"],
            taxable_income,
        )
    elif taxable_income <= tax_curve[YEAR][3]["step"]:
        return tax_curve[YEAR][2]["rate"]
    else:
        return tax_curve[YEAR][3]["rate"]


def __calc_gradient(x_i, x_j, y_i, y_j, x):
    return (1 - (x_j - x) / (x_j - x_i)) * (y_j - y_i) + y_i


def calc_taxable_income(salary, deductable_social_security, deductable_other=0):
    return math.floor(
        max(0, salary - deductable_social_security - 1200 - 36 - deductable_other)
    )


if __name__ == "__main__":
    print(get_marginal_tax_rate(50000))
