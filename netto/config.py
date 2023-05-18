import os


def str_to_bool(s):
    if s == "True":
        return True
    elif s == "False":
        return False
    else:
        raise ValueError


# Use default values if environment variables are not set or are set to invalid values
def load_config():
    global year, has_children, is_married, extra_health_insurance, church_tax

    try:
        year = int(os.getenv("YEAR", "2022"))
    except ValueError:
        year = 2022

    try:
        has_children = str_to_bool(os.getenv("HAS_CHILDREN", "False"))
    except ValueError:
        has_children = False

    try:
        is_married = str_to_bool(os.getenv("IS_MARRIED", "False"))
    except ValueError:
        is_married = False

    try:
        extra_health_insurance = float(os.getenv("EXTRA_HEALTH_INSURANCE", "0.014"))
    except ValueError:
        extra_health_insurance = 0.014

    try:
        church_tax = float(os.getenv("CHURCH_TAX", "0.09"))
    except ValueError:
        church_tax = 0.09


load_config()
