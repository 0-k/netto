import numpy as np
import matplotlib.pyplot as plt
from netto.taxes_income import calc_taxable_income, calc_income_tax_by_integration
from netto.taxes_other import calc_soli, calc_church_tax
from netto.social_security import calc_deductable_social_security, calc_social_security
import netto.config as config


def calc_netto(salary):
    deductable_social_security = calc_deductable_social_security(salary)
    taxable_income = calc_taxable_income(
        salary=salary, deductable_social_security=deductable_social_security
    )
    income_tax = calc_income_tax_by_integration(taxable_income)
    return (
        salary
        - income_tax
        - calc_soli(income_tax)
        - calc_church_tax(income_tax)
        - calc_social_security(salary)
    )


if __name__ == "__main__":
    config.YEAR = 2022
    net_2022 = [calc_netto(salary) for salary in range(0, 200001, 1000)]
    config.YEAR = 2023
    net_2023 = [calc_netto(salary) for salary in range(0, 200001, 1000)]
    plt.plot(np.array(net_2023) - np.array(net_2022))
    plt.show()
