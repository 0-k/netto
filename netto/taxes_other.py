import netto.config as config
from netto.const import soli_curve


def calc_soli(tax_assessment):
    return round(
        max(
            min(
                max(0, tax_assessment - soli_curve[config.year]["start_taxable_income"])
                * soli_curve[config.year]["start_fraction"],
                tax_assessment * soli_curve[config.year]["end_rate"],
            ),
            0,
        ),
        2,
    )


def calc_church_tax(tax_assessment):
    return round(max(tax_assessment * config.church_tax, 0), 2)
