from netto.taxes_income import calc_taxable_income
from netto.social_security import calc_deductable_social_security

def run(salary):
    salary = 5881 * 12

    duck = calc_deductable_social_security(salary)
    taxable_income = calc_taxable_income(salary=salary,
                                         deductable_social_security=duck)

    print(salary / 12 - calc_income_tax_by_integration(
        taxable_income) / 12 - calc_social_security(salary) / 12)


if __name__ == "__main__":
    run()
