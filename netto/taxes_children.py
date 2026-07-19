from netto.config import TaxConfig
from netto.data_loader import child_benefits as CHILD_BENEFITS_DATA
from netto.taxes_income import calc_income_tax_by_integration


def calc_kindergeld(config: TaxConfig | None = None) -> float:
    """
    Calculate the yearly Kindergeld for all children in the configuration.

    Uses the first/second-child rate for every child (before 2023 the third
    and further children received slightly more; one-off Corona bonuses are
    not included).

    Parameters
    ----------
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Total yearly Kindergeld

    Examples
    --------
    >>> calc_kindergeld(TaxConfig(year=2026, num_children=2))
    6216.0
    """
    if config is None:
        config = TaxConfig()

    return (
        CHILD_BENEFITS_DATA[config.year]["kindergeld_per_child"] * config.num_children
    )


def calc_child_allowance_per_child(config: TaxConfig | None = None) -> float:
    """
    Yearly child allowance (Kinderfreibetrag incl. BEA) per child.

    Married couples under joint assessment receive the full allowance; a
    single parent receives half (the other half belongs to the other
    parent). The Übertragung of the other parent's half is not modeled.

    Parameters
    ----------
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Yearly child allowance per child
    """
    if config is None:
        config = TaxConfig()

    full = CHILD_BENEFITS_DATA[config.year]["kinderfreibetrag_per_child"]
    return full if config.is_married else full / 2


def apply_guenstigerpruefung(
    taxable_income: float, income_tax: float, config: TaxConfig | None = None
) -> tuple[float, float]:
    """
    Apply the per-child Günstigerprüfung (Kindergeld vs. Kinderfreibetrag).

    For each child (checked sequentially against a taxable income already
    reduced by the previous children's allowances), the tax relief of the
    child allowance is compared with the Kindergeld entitlement. If the
    relief is larger, the allowance is deducted and the Kindergeld is added
    back to the tax liability (Hinzurechnung, § 31 EStG) - so together with
    the Kindergeld paid out, the family keeps the full allowance benefit.

    Solidarity surcharge and church tax are always based on the fictitious
    income tax with ALL child allowances deducted (§ 3 SolzG, § 51a EStG),
    regardless of the Günstigerprüfung outcome.

    Parameters
    ----------
    taxable_income : float
        Taxable income before child allowances
    income_tax : float
        Income tax on taxable_income (before child allowances)
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    tuple[float, float]
        (assessed income tax after the Günstigerprüfung including the
        Kindergeld Hinzurechnung, fictitious income tax with all child
        allowances deducted - the base for soli and church tax)
    """
    if config is None:
        config = TaxConfig()

    if config.num_children == 0:
        return income_tax, income_tax

    allowance = calc_child_allowance_per_child(config)
    # A single parent claims half the allowance, so only half the
    # Kindergeld is counted against it (§ 31 S. 4 EStG).
    kindergeld_per_child = CHILD_BENEFITS_DATA[config.year]["kindergeld_per_child"] * (
        1 if config.is_married else 0.5
    )

    assessed_tax = income_tax
    remaining_income = taxable_income
    tax_before_child = income_tax
    for _ in range(config.num_children):
        remaining_income = max(0, remaining_income - allowance)
        tax_after_child = calc_income_tax_by_integration(remaining_income, config)
        relief = tax_before_child - tax_after_child
        if relief > kindergeld_per_child:
            assessed_tax += kindergeld_per_child - relief
        tax_before_child = tax_after_child

    fictitious_tax = tax_before_child
    return assessed_tax, fictitious_tax
