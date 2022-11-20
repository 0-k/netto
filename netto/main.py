from scipy.optimize import newton
from .taxes_income import calc_taxable_income, calc_income_tax_by_integration
from .taxes_other import calc_soli, calc_church_tax
from .social_security import calc_deductable_social_security, calc_social_security


def calc_netto(salary, deductable_other=0):
    deductable_social_security = calc_deductable_social_security(salary)
    taxable_income = calc_taxable_income(
        salary=salary,
        deductable_social_security=deductable_social_security,
        deductable_other=deductable_other,
    )
    income_tax = calc_income_tax_by_integration(taxable_income)
    return round(
        (
            salary
            - income_tax
            - calc_soli(income_tax)
            - calc_church_tax(income_tax)
            - calc_social_security(salary)
        ),
        2,
    )


def calc_inverse_netto(desired_netto, deductable_other=10000):
    """find gross salary to reach desired netto"""

    def f(salary):
        return calc_netto(salary, deductable_other=deductable_other) - desired_netto

    return round(newton(f, x0=desired_netto), 0)


if __name__ == "__main__":
    print("hello world")
