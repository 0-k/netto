import math
from typing import Optional

from scipy.integrate import quad

from netto.config import TaxConfig, get_default_config
from netto.const import __correction_factor_pensions, __social_security_curve


def get_rate_pension(salary: float, config: Optional[TaxConfig] = None) -> float:
    return __get_rate(salary, "pension", config=config)


def __get_rate(salary: float, type: str, extra: float = 0, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    return (
        __social_security_curve[config.year][type]["rate"] + extra
        if 0 < salary <= __social_security_curve[config.year][type]["limit"]
        else 0
    )


def get_rate_unemployment(salary: float, config: Optional[TaxConfig] = None) -> float:
    return __get_rate(salary, "unemployment", config=config)


def get_rate_health(salary: float, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    extra = config.extra_health_insurance / 2
    return __get_rate(salary, "health", extra, config=config)


def get_rate_nursing(salary: float, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    extra = (
        0
        if config.has_children
        else __social_security_curve[config.year]["nursing"]["extra"]
    )
    return __get_rate(salary, "nursing", extra, config=config)


def calc_insurance_pension(salary: float, config: Optional[TaxConfig] = None) -> float:
    return __get_value(salary, "pension", config=config)


def __get_value(salary: float, type: str, extra: float = 0, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    return min(
        salary * (__social_security_curve[config.year][type]["rate"] + extra),
        __social_security_curve[config.year][type]["limit"]
        * (__social_security_curve[config.year][type]["rate"] + extra),
    )


def calc_insurance_unemployment(salary: float, config: Optional[TaxConfig] = None) -> float:
    return __get_value(salary, "unemployment", config=config)


def calc_insurance_health(salary: float, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    extra = config.extra_health_insurance / 2
    return __get_value(salary, "health", extra, config=config)


def calc_insurance_health_deductable(salary: float, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    extra = config.extra_health_insurance / 2
    return __get_value(salary, "health", extra - 0.003, config=config)


def calc_insurance_nursing(salary: float, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    extra = (
        0
        if config.has_children
        else __social_security_curve[config.year]["nursing"]["extra"]
    )
    return __get_value(salary, "nursing", extra, config=config)


def calc_deductible_social_security(salary: float, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    return (
        math.ceil(
            calc_insurance_pension(salary, config) * __correction_factor_pensions[config.year]
        )
        + math.ceil(calc_insurance_health_deductable(salary, config))
        + math.ceil(calc_insurance_nursing(salary, config))
    )


def calc_social_security(salary: float, config: Optional[TaxConfig] = None) -> float:
    return round(
        calc_insurance_pension(salary, config)
        + calc_insurance_health(salary, config)
        + calc_insurance_nursing(salary, config)
        + calc_insurance_unemployment(salary, config),
        2,
    )


def calc_social_security_by_integration(salary: float, config: Optional[TaxConfig] = None) -> float:
    if config is None:
        config = get_default_config()
    pension, _ = quad(lambda s: get_rate_pension(s, config), 0, salary)
    health, _ = quad(lambda s: get_rate_health(s, config), 0, salary)
    nursing, _ = quad(lambda s: get_rate_nursing(s, config), 0, salary)
    unemployment, _ = quad(lambda s: get_rate_unemployment(s, config), 0, salary)
    return round(pension + health + nursing + unemployment, 2)
