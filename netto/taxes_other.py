from netto.config import CHURCH_TAX


def calc_soli(tax_assessment):
    return min(max(0, tax_assessment - 16956) * 0.119, tax_assessment * 0.055)


def calc_church_tax(tax_assessment):
    return tax_assessment * CHURCH_TAX
