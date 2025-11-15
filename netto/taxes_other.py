from netto.config import TaxConfig
from netto.data_loader import soli_curve


def calc_soli(tax_assessment: float, config: TaxConfig | None = None) -> float:
    """
    Calculate solidarity tax (Solidaritätszuschlag).

    Parameters
    ----------
    tax_assessment : float
        The income tax assessment base
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        The solidarity tax amount
    """
    if config is None:
        config = TaxConfig()

    return round(
        max(
            min(
                max(
                    0,
                    tax_assessment - soli_curve[config.year]["start_taxable_income"],
                )
                * soli_curve[config.year]["start_fraction"],
                tax_assessment * soli_curve[config.year]["end_rate"],
            ),
            0,
        ),
        2,
    )


def calc_church_tax(tax_assessment: float, config: TaxConfig | None = None) -> float:
    """
    Calculate church tax (Kirchensteuer).

    Parameters
    ----------
    tax_assessment : float
        The income tax assessment base
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        The church tax amount
    """
    if config is None:
        config = TaxConfig()

    return round(max(tax_assessment * config.church_tax, 0), 2)
