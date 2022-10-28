def get_rate_pension(salary):
    return 0.093 if salary <= 84600 else 0


def get_rate_unemployment(salary):
    return 0.012 if salary <= 84600 else 0


def get_rate_health(salary):
    return 0.073 + 0.013 / 2 if salary <= 58050 else 0


def get_rate_nursing(salary):
    return 0.01525 if salary <= 58050 else 0


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
