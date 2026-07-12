from scipy.optimize import newton

from netto.config import TaxConfig
from netto.social_security import calc_deductible_social_security, calc_social_security
from netto.taxes_children import apply_guenstigerpruefung, calc_kindergeld
from netto.taxes_income import calc_income_tax_by_integration, calc_taxable_income
from netto.taxes_other import calc_church_tax, calc_soli


def calc_netto(
    salary: float,
    deductibles: float = 0,
    verbose: bool = False,
    config: TaxConfig | None = None,
    partner_salary: float = 0,
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
    if partner_salary < 0:
        raise ValueError(f"partner_salary must be non-negative, got {partner_salary}")
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
    income_tax = calc_income_tax_by_integration(taxable_income, config)
    kindergeld = calc_kindergeld(config)
    income_tax, fictitious_tax = apply_guenstigerpruefung(
        taxable_income, income_tax, config
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


def calc_inverse_netto(
    desired_netto: float,
    deductibles: float = 0,
    config: TaxConfig | None = None,
    partner_salary: float = 0,
) -> float:
    """
    Calculate required gross salary to reach desired net income.

    If ``partner_salary`` is given, it is kept fixed and the primary salary
    required to reach the desired household net income is calculated.

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

    Returns
    -------
    float
        Required gross salary

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

    if partner_salary > 0:
        netto_without_primary = calc_netto(
            0, deductibles=deductibles, config=config, partner_salary=partner_salary
        )
        if desired_netto <= netto_without_primary:
            raise ValueError(
                f"desired_netto {desired_netto} is already reached by the "
                f"partner salary alone (household netto without primary "
                f"salary: {netto_without_primary})"
            )

    def f(salary):
        return (
            calc_netto(
                salary,
                deductibles=deductibles,
                config=config,
                partner_salary=partner_salary,
            )
            - desired_netto
        )

    return round(newton(f, x0=max(desired_netto - partner_salary, 1)), 0)
