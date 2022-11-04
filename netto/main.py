from netto.taxes_income import calc_taxable_income, calc_income_tax_by_integration
from netto.taxes_other import calc_soli, calc_church_tax
from netto.social_security import calc_deductable_social_security, calc_social_security


def run(salary):
    deductable_social_security = calc_deductable_social_security(salary)
    taxable_income = calc_taxable_income(
        salary=salary, deductable_social_security=deductable_social_security
    )

    income_tax = calc_income_tax_by_integration(taxable_income)

    print(
        salary / 12
        - income_tax / 12
        - calc_soli(income_tax) / 12
        - calc_church_tax(income_tax) / 12
        - calc_social_security(salary) / 12
    )


if __name__ == "__main__":
    run(5881*12)
