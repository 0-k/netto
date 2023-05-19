from scipy.optimize import newton

from netto.social_security import calc_deductible_social_security, calc_social_security
from netto.taxes_income import calc_income_tax_by_integration, calc_taxable_income
from netto.taxes_other import calc_church_tax, calc_soli


def calc_netto(salary, deductibles=0, verbose=False):
    """
    This function calculates the net income for a given year by subtracting the income tax, soli, church tax, and social security amounts from the salary.

    Parameters
    ----------
    salary: float or int
        The yearly salary.
    deductibles: float or int, optional
        Deductibles that reduce the taxable income. Default is 0.
    verbose: bool, optional
        Determines whether additional information about the calculation should be printed. Default is False.

    Returns
    -------
    net_income: float
        The net income for a given year.

    Examples
    --------
    # Calculate net income for a salary of 50,000 with no additional deductibles
    calc_netto(50000)

    # Calculate net income for a salary of 50,000 with additional deductibles of 10,000
    calc_netto(50000, deductibles=10000)

    # Calculate net income for a salary of 50,000 and print additional information
    calc_netto(50000, verbose=True)
    """

    deductible_social_security = calc_deductible_social_security(salary)
    taxable_income = calc_taxable_income(
        salary=salary,
        deductible_social_security=deductible_social_security,
        deductibles_other=deductibles,
    )
    income_tax = calc_income_tax_by_integration(taxable_income)
    if verbose:
        repr = (
            "Yearly Evaluation:\n"
            + f"Income Tax:      {round(income_tax, 2):>12}\n"
            + f"Soli:            {round(calc_soli(income_tax), 2):>12}\n"
            + f"Church Tax:      {round(calc_church_tax(income_tax), 2):>12}\n"
            + f"Social Security: {round(calc_social_security(salary), 2):>12}"
        )
        print(repr)
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


def calc_inverse_netto(desired_netto, deductibles=0):
    """
    Calculate gross salary to reach desired net income.

    This function calculates the gross salary needed to reach a desired net income. It uses the `calc_netto()` function to calculate the net income for a given salary, and then uses the `newton()` function to find the salary that produces the desired net income.

    Parameters
    ----------
    desired_netto: float or int
        The desired net income.
    deductibles: float or int, optional
        Deductibles that reduce the taxable income. Default is 0.

    Returns
    -------
    gross_salary: float
        The gross salary needed to reach the desired net income.

    Examples
    --------
    # Calculate gross salary needed to reach a net income of 50,000 with no additional deductibles
    calc_inverse_netto(50000)

    # Calculate gross salary needed to reach a net income of 50,000 with additional deductibles of 5,000
    calc_inverse_netto(50000, deductable_other=5000)
    """

    def f(salary):
        return calc_netto(salary, deductibles=deductibles) - desired_netto

    return round(newton(f, x0=desired_netto), 0)
