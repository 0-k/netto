import math

from scipy.integrate import quad

import netto.config as config
from netto.const import __correction_factor_pensions, __social_security_curve


def get_rate_pension(salary):
    return __get_rate(salary, "pension")


def __get_rate(salary, type, extra=0):
    return (
        __social_security_curve[config.year][type]["rate"] + extra
        if 0 < salary <= __social_security_curve[config.year][type]["limit"]
        else 0
    )


def get_rate_unemployment(salary):
    return __get_rate(salary, "unemployment")


def get_rate_health(salary):
    extra = config.extra_health_insurance / 2
    return __get_rate(salary, "health", extra)


def get_rate_nursing(salary):
    extra = (
        0
        if config.has_children
        else __social_security_curve[config.year]["nursing"]["extra"]
    )
    return __get_rate(salary, "nursing", extra)


def calc_insurance_pension(salary):
    return __get_value(salary, "pension")


def __get_value(salary, type, extra=0):
    return min(
        salary * (__social_security_curve[config.year][type]["rate"] + extra),
        __social_security_curve[config.year][type]["limit"]
        * (__social_security_curve[config.year][type]["rate"] + extra),
    )


def calc_insurance_unemployment(salary):
    return __get_value(salary, "unemployment")


def calc_insurance_health(salary):
    extra = config.extra_health_insurance / 2
    return __get_value(salary, "health", extra)


def calc_insurance_health_deductable(salary):
    extra = config.extra_health_insurance / 2
    return __get_value(salary, "health", extra - 0.003)


def calc_insurance_nursing(salary):
    extra = (
        0
        if config.has_children
        else __social_security_curve[config.year]["nursing"]["extra"]
    )
    return __get_value(salary, "nursing", extra)


def calc_deductible_social_security(salary):
    return (
        math.ceil(
            calc_insurance_pension(salary) * __correction_factor_pensions[config.year]
        )
        + math.ceil(calc_insurance_health_deductable(salary))
        + math.ceil(calc_insurance_nursing(salary))
    )


def calc_social_security(salary):
    return round(
        calc_insurance_pension(salary)
        + calc_insurance_health(salary)
        + calc_insurance_nursing(salary)
        + calc_insurance_unemployment(salary),
        2,
    )


def calc_social_security_by_integration(salary):
    pension, _ = quad(get_rate_pension, 0, salary)
    health, _ = quad(get_rate_health, 0, salary)
    nursing, _ = quad(get_rate_nursing, 0, salary)
    unemployment, _ = quad(get_rate_unemployment, 0, salary)
    return round(pension + health + nursing + unemployment, 2)
