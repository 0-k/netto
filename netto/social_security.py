import math
from const import social_security_curve
from config import YEAR, HAS_CHILDREN


def __get_rate(salary, type, extra=0):
    return (
        social_security_curve[YEAR][type]["rate"] + extra
        if salary <= social_security_curve[YEAR][type]["limit"]
        else 0
    )


def get_marginal_rate_pension(salary):
    return __get_rate(salary, "pension")


def get_rate_unemployment(salary):
    return __get_rate(salary, "unemployment")


def get_rate_health(salary):
    extra = social_security_curve[YEAR]["nursing"]["extra"]
    return __get_rate(salary, "health", extra)


def get_rate_nursing(salary):
    extra = 0 if HAS_CHILDREN else social_security_curve[YEAR]["nursing"]["extra"]
    return __get_rate(salary, "nursing", extra)


def calc_insurance_pension(salary):
    return min(salary * 0.093, 84600 * 0.093)


def calc_insurance_health(salary, extra=0.012 / 2):
    return min(salary * (0.073 + extra), 58050 * (0.073 + extra))


def calc_insurance_unemployment(salary):
    return min(salary * 0.012, 84600 * 0.012)


def calc_insurance_nursing(salary, no_child_extra=0.0):
    return min(salary * (0.01525 + no_child_extra), 58050 * (0.01525 + no_child_extra))


def calc_deductable_social_security(salary):
    return (
        calc_insurance_pension(salary) * 0.88
        + calc_insurance_health(salary)
        + calc_insurance_nursing(salary)
    )


def calc_social_security(salary):
    return (
        calc_insurance_pension(salary)
        + calc_insurance_health(salary)
        + calc_insurance_nursing(salary)
        + calc_insurance_unemployment(salary)
    )
