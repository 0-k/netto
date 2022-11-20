import netto.config as config
from .const import soli_curve


def calc_soli(tax_assessment):
    return round(
        max(
            min(
                max(0, tax_assessment - soli_curve[config.YEAR]["start_taxable_income"])
                * soli_curve[config.YEAR]["start_fraction"],
                tax_assessment * soli_curve[config.YEAR]["end_rate"],
            ),
            0,
        ),
        2,
    )


def calc_church_tax(tax_assessment):
    return round(max(tax_assessment * config.CHURCH_TAX, 0), 2)
