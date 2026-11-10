from scipy.optimize import brentq

from netto.config import TaxConfig
from netto.social_security import calc_deductible_social_security, calc_social_security
from netto.taxes_children import apply_guenstigerpruefung, calc_kindergeld
from netto.taxes_income import calc_income_tax_with_progression, calc_taxable_income
from netto.taxes_other import calc_church_tax, calc_soli


def calc_netto(
    salary: float,
    deductibles: float = 0,
    verbose: bool = False,
    config: TaxConfig | None = None,
    partner_salary: float = 0,
    progression_income: float = 0,
) -> float:
    """
    Calculate net income from gross salary.

    For dual-income married couples, pass the spouse's salary as
    ``partner_salary``. Income tax is then assessed jointly
    (Ehegattensplitting) while social security contributions are calculated
    per person against the individual contribution ceilings. The returned
    value is the combined household net income.

    With ``num_children`` set in the config, the result includes the yearly
    Kindergeld and applies the Günstigerprüfung: if the Kinderfreibetrag
    yields more tax relief than the Kindergeld, the allowance is deducted
    and the Kindergeld added back to the tax (§ 31 EStG). Solidarity
    surcharge and church tax are always based on the income tax with child
    allowances deducted.

    Parameters
    ----------
    salary: float
        Yearly gross salary
    deductibles: float, optional
        Additional deductibles that reduce taxable income
    verbose: bool, optional
        Print detailed calculation breakdown
    config : TaxConfig, optional
        Tax configuration (uses defaults if not provided)
    partner_salary: float, optional
        Yearly gross salary of the spouse (requires is_married=True).
        Default is 0 (single-earner household).
    progression_income: float, optional
        Yearly tax-free replacement benefits under the Progressionsvorbehalt
        (§ 32b EStG), e.g. Elterngeld. They are NOT added to the result
        (add them yourself); they raise the tax rate on the taxable income.

    Returns
    -------
    float
        Net income (household net income if partner_salary is given;
        includes Kindergeld if num_children is set)

    Examples
    --------
    >>> calc_netto(50000)
    >>> calc_netto(50000, deductibles=10000)
    >>> calc_netto(50000, verbose=True)
    >>> config = TaxConfig(year=2025, is_married=True)
    >>> calc_netto(50000, config=config)
    >>> calc_netto(50000, config=config, partner_salary=40000)
    """
    if config is None:
        config = TaxConfig()
    if salary < 0:
        raise ValueError(f"salary must be non-negative, got {salary}")
    if deductibles < 0:
        raise ValueError(f"deductibles must be non-negative, got {deductibles}")
    if partner_salary < 0:
        raise ValueError(f"partner_salary must be non-negative, got {partner_salary}")
    if progression_income < 0:
        raise ValueError(
            f"progression_income must be non-negative, got {progression_income}"
        )
    if partner_salary > 0 and not config.is_married:
        raise ValueError(
            "partner_salary requires is_married=True, as only jointly "
            "assessed couples are taxed on their combined income"
        )

    deductible_social_security = calc_deductible_social_security(salary, config)
    social_security = calc_social_security(salary, config)
    if partner_salary > 0:
        deductible_social_security += calc_deductible_social_security(
            partner_salary, config
        )
        social_security += calc_social_security(partner_salary, config)
    taxable_income = calc_taxable_income(
        salary=salary,
        deductible_social_security=deductible_social_security,
        deductibles_other=deductibles,
        config=config,
        partner_salary=partner_salary,
    )
    income_tax = calc_income_tax_with_progression(
        taxable_income, progression_income, config
    )
    kindergeld = calc_kindergeld(config)
    income_tax, fictitious_tax = apply_guenstigerpruefung(
        taxable_income, income_tax, config, progression_income
    )
    soli = calc_soli(fictitious_tax, config)
    church_tax = calc_church_tax(fictitious_tax, config)
    if verbose:
        repr = (
            "Yearly Evaluation:\n"
            + f"Income Tax:      {round(income_tax, 2):>12}\n"
            + f"Soli:            {round(soli, 2):>12}\n"
            + f"Church Tax:      {round(church_tax, 2):>12}\n"
            + f"Social Security: {round(social_security, 2):>12}"
        )
        if config.num_children > 0:
            repr += f"\nKindergeld:      {round(kindergeld, 2):>12}"
        print(repr)
    return round(
        salary
        + partner_salary
        + kindergeld
        - income_tax
        - soli
        - church_tax
        - social_security,
        2,
    )


# Upper end of the search bracket for calc_inverse_netto is doubled until it
# nets more than the target; this caps the number of doublings.
_MAX_BRACKET_DOUBLINGS = 60


def calc_inverse_netto(
    desired_netto: float,
    deductibles: float = 0,
    config: TaxConfig | None = None,
    partner_salary: float = 0,
    progression_income: float = 0,
) -> float:
    """
    Calculate required gross salary to reach desired net income.

    If ``partner_salary`` is given, it is kept fixed and the primary salary
    required to reach the desired household net income is calculated.

    The net income is a step function of the gross salary (cent rounding,
    taxable income floored to full euros), so the salary is found with a
    bracketing root finder and rounded to full euros; ``calc_netto`` of the
    result is within a few euros of ``desired_netto``.

    Parameters
    ----------
    desired_netto: float
        Desired net income
    deductibles: float, optional
        Additional deductibles that reduce taxable income
    config : TaxConfig, optional
        Tax configuration (uses defaults if not provided)
    partner_salary: float, optional
        Fixed yearly gross salary of the spouse (requires is_married=True)
    progression_income: float, optional
        Yearly tax-free benefits under the Progressionsvorbehalt
        (§ 32b EStG), passed through to ``calc_netto``

    Returns
    -------
    float
        Required gross salary, rounded to full euros

    Raises
    ------
    ValueError
        If ``desired_netto`` is below the net income at zero salary, i.e.
        already reached by the partner salary alone and/or the Kindergeld

    Examples
    --------
    >>> calc_inverse_netto(50000)
    >>> calc_inverse_netto(50000, deductibles=5000)
    >>> config = TaxConfig(year=2025, is_married=True)
    >>> calc_inverse_netto(50000, config=config)
    >>> calc_inverse_netto(70000, config=config, partner_salary=40000)
    """
    if config is None:
        config = TaxConfig()

    def f(salary):
        return (
            calc_netto(
                salary,
                deductibles=deductibles,
                config=config,
                partner_salary=partner_salary,
                progression_income=progression_income,
            )
            - desired_netto
        )

    netto_without_primary = f(0) + desired_netto
    if desired_netto < netto_without_primary:
        raise ValueError(
            f"desired_netto {desired_netto} is already reached by the "
            f"partner salary alone and/or the Kindergeld (household netto "
            f"without primary salary: {netto_without_primary})"
        )
    if desired_netto == netto_without_primary:
        return 0.0

    upper = max(desired_netto - netto_without_primary, 1.0)
    for _ in range(_MAX_BRACKET_DOUBLINGS):
        upper *= 2
        if f(upper) >= 0:
            break
    else:
        raise ValueError(f"desired_netto {desired_netto} cannot be reached")
    # xtol well below one euro: the result is rounded to full euros anyway
    return float(round(brentq(f, 0, upper, xtol=1e-3), 0))
