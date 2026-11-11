import math

from scipy.integrate import quad

from netto.config import TaxConfig
from netto.data_loader import correction_factor_pensions, social_security_curve

# Pflegeversicherung child discount (§ 55 Abs. 3 SGB XI, PUEG, from
# 2023-07-01): members with at least two children under 25 pay 0.25 pp
# less (employee share) for the 2nd to 5th child.
NURSING_CHILD_DISCOUNT = 0.0025
NURSING_CHILD_DISCOUNT_MAX_CHILDREN = 4

# Health Zusatzbeitrag: paid by the employee alone until 2018, shared
# equally with the employer since 2019-01-01 (GKV-Versichertenentlastungsgesetz).
HEALTH_EXTRA_PARITY_FROM_YEAR = 2019


def _nursing_child_discount(config: TaxConfig) -> float:
    """Employee-share reduction of the nursing rate for 2+ children.

    Uses ``num_children`` (Kindergeld-eligible children, i.e. usually under
    25). 2023 gets half the yearly effect (in force from July).
    """
    if config.year < 2023:
        return 0.0
    extra_children = min(
        max(config.num_children - 1, 0), NURSING_CHILD_DISCOUNT_MAX_CHILDREN
    )
    discount = extra_children * NURSING_CHILD_DISCOUNT
    return discount / 2 if config.year == 2023 else discount


def _health_extra_employee_share(config: TaxConfig) -> float:
    """Employee share of the health Zusatzbeitrag as a rate on the salary.

    Takes the explicit ``config.extra_health_insurance`` or, if that is
    None, the official year-specific average from the data files. The
    employee pays all of it until 2018 and half of it from 2019.
    """
    total = (
        config.extra_health_insurance
        if config.extra_health_insurance is not None
        else social_security_curve[config.year]["health"]["extra"]
    )
    return total if config.year < HEALTH_EXTRA_PARITY_FROM_YEAR else total / 2


def _nursing_extra(config: TaxConfig) -> float:
    """Childless surcharge, or the (negative) discount for 2+ children."""
    if config.has_children:
        return -_nursing_child_discount(config)
    return social_security_curve[config.year]["nursing"]["extra"]


def __get_rate(
    salary: float, type: str, extra: float = 0, config: TaxConfig | None = None
) -> float:
    if config is None:
        config = TaxConfig()
    return (
        social_security_curve[config.year][type]["rate"] + extra
        if 0 < salary <= social_security_curve[config.year][type]["limit"]
        else 0
    )


def __get_value(
    salary: float, type: str, extra: float = 0, config: TaxConfig | None = None
) -> float:
    if config is None:
        config = TaxConfig()
    return min(
        salary * (social_security_curve[config.year][type]["rate"] + extra),
        social_security_curve[config.year][type]["limit"]
        * (social_security_curve[config.year][type]["rate"] + extra),
    )


def get_rate_pension(salary: float, config: TaxConfig | None = None) -> float:
    """
    Marginal employee pension insurance rate at a given salary.

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Employee contribution rate as a fraction of salary; 0 for a salary
        of 0 or above the contribution ceiling (Beitragsbemessungsgrenze)

    Examples
    --------
    >>> get_rate_pension(50000, TaxConfig(year=2025))
    0.093
    """
    return __get_rate(salary, "pension", config=config)


def get_rate_unemployment(salary: float, config: TaxConfig | None = None) -> float:
    """
    Marginal employee unemployment insurance rate at a given salary.

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Employee contribution rate as a fraction of salary; 0 for a salary
        of 0 or above the contribution ceiling

    Examples
    --------
    >>> get_rate_unemployment(50000, TaxConfig(year=2025))
    0.013
    """
    return __get_rate(salary, "unemployment", config=config)


def get_rate_health(salary: float, config: TaxConfig | None = None) -> float:
    """
    Marginal employee health insurance rate at a given salary.

    Includes the employee share of the Zusatzbeitrag (half of it from 2019,
    all of it in 2018).

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Employee contribution rate as a fraction of salary; 0 for a salary
        of 0 or above the contribution ceiling

    Examples
    --------
    >>> get_rate_health(50000, TaxConfig(year=2025, extra_health_insurance=0.02))
    """
    if config is None:
        config = TaxConfig()
    return __get_rate(
        salary, "health", _health_extra_employee_share(config), config=config
    )


def get_rate_nursing(salary: float, config: TaxConfig | None = None) -> float:
    """
    Marginal employee nursing care insurance rate at a given salary.

    Includes the childless surcharge (``has_children=False``) or the
    discount for the 2nd to 5th child (``num_children``, from 2023).

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Employee contribution rate as a fraction of salary; 0 for a salary
        of 0 or above the contribution ceiling

    Examples
    --------
    >>> get_rate_nursing(50000, TaxConfig(year=2025, has_children=True))
    0.018
    """
    if config is None:
        config = TaxConfig()
    return __get_rate(salary, "nursing", _nursing_extra(config), config=config)


def calc_insurance_pension(salary: float, config: TaxConfig | None = None) -> float:
    """
    Yearly employee pension insurance contribution.

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Contribution in EUR, capped at the contribution ceiling

    Examples
    --------
    >>> calc_insurance_pension(50000, TaxConfig(year=2025))
    4650.0
    """
    return __get_value(salary, "pension", config=config)


def calc_insurance_unemployment(
    salary: float, config: TaxConfig | None = None
) -> float:
    """
    Yearly employee unemployment insurance contribution.

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Contribution in EUR, capped at the contribution ceiling

    Examples
    --------
    >>> calc_insurance_unemployment(50000, TaxConfig(year=2025))
    650.0
    """
    return __get_value(salary, "unemployment", config=config)


def calc_insurance_health(salary: float, config: TaxConfig | None = None) -> float:
    """
    Yearly employee health insurance contribution.

    Includes the employee share of the Zusatzbeitrag (half of it from 2019,
    all of it in 2018).

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Contribution in EUR, capped at the contribution ceiling

    Examples
    --------
    >>> calc_insurance_health(50000, TaxConfig(year=2025))
    """
    if config is None:
        config = TaxConfig()
    return __get_value(
        salary, "health", _health_extra_employee_share(config), config=config
    )


def calc_insurance_health_deductable(
    salary: float, config: TaxConfig | None = None
) -> float:
    """
    Tax-deductible part of the yearly employee health insurance contribution.

    The share that finances the Krankengeld entitlement is not deductible
    (§ 10 Abs. 1 Nr. 3 EStG); it is approximated as 0.3 percentage points.

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Deductible contribution in EUR

    Examples
    --------
    >>> calc_insurance_health_deductable(50000, TaxConfig(year=2025))
    """
    if config is None:
        config = TaxConfig()
    return __get_value(
        salary, "health", _health_extra_employee_share(config) - 0.003, config=config
    )


def calc_insurance_nursing(salary: float, config: TaxConfig | None = None) -> float:
    """
    Yearly employee nursing care insurance contribution.

    Includes the childless surcharge (``has_children=False``) or the
    discount for the 2nd to 5th child (``num_children``, from 2023).

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Contribution in EUR, capped at the contribution ceiling

    Examples
    --------
    >>> calc_insurance_nursing(50000, TaxConfig(year=2025, has_children=True))
    """
    if config is None:
        config = TaxConfig()
    return __get_value(salary, "nursing", _nursing_extra(config), config=config)


def calc_deductible_social_security(
    salary: float, config: TaxConfig | None = None
) -> float:
    """
    Social security contributions deductible as Vorsorgeaufwendungen.

    Sum of the pension contribution (times the year's deduction factor),
    the deductible health contribution and the nursing contribution, each
    rounded up to full euros. Unemployment insurance is not included.

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Deductible contributions in EUR

    Examples
    --------
    >>> calc_deductible_social_security(50000, TaxConfig(year=2025))
    """
    if config is None:
        config = TaxConfig()
    return (
        math.ceil(
            calc_insurance_pension(salary, config)
            * correction_factor_pensions[config.year]
        )
        + math.ceil(calc_insurance_health_deductable(salary, config))
        + math.ceil(calc_insurance_nursing(salary, config))
    )


def calc_social_security(salary: float, config: TaxConfig | None = None) -> float:
    """
    Total yearly employee social security contributions.

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Pension, health, nursing and unemployment contributions in EUR,
        rounded to cents

    Examples
    --------
    >>> calc_social_security(50000, TaxConfig(year=2025))
    """
    return round(
        calc_insurance_pension(salary, config)
        + calc_insurance_health(salary, config)
        + calc_insurance_nursing(salary, config)
        + calc_insurance_unemployment(salary, config),
        2,
    )


def calc_social_security_by_integration(
    salary: float, config: TaxConfig | None = None
) -> float:
    """
    Total employee social security by integrating the marginal rates.

    Cross-check for ``calc_social_security``. Each rate is integrated only
    up to its contribution ceiling, above which it is zero.

    Parameters
    ----------
    salary : float
        Yearly gross salary
    config : TaxConfig, optional
        Tax configuration (uses default if not provided)

    Returns
    -------
    float
        Total contributions in EUR, rounded to cents

    Examples
    --------
    >>> calc_social_security_by_integration(50000, TaxConfig(year=2025))
    """
    if config is None:
        config = TaxConfig()
    limits = social_security_curve[config.year]
    total = 0.0
    for type, get_rate in (
        ("pension", get_rate_pension),
        ("health", get_rate_health),
        ("nursing", get_rate_nursing),
        ("unemployment", get_rate_unemployment),
    ):
        value, _ = quad(
            lambda s, get_rate=get_rate: get_rate(s, config),
            0,
            min(salary, limits[type]["limit"]),
        )
        total += value
    return round(total, 2)
