import os


YEAR = 2022 if os.getenv("YEAR") is None else int(os.getenv("YEAR"))
HAS_CHILDREN = (
    False if os.getenv("HAS_CHILDREN") is None else bool(os.getenv("HAS_CHILDREN"))
)
EXTRA_HEALTH_INSURANCE = (
    0.013 / 2
    if os.getenv("EXTRA_HEALTH_INSURANCE") is None
    else float(os.getenv("EXTRA_HEALTH_INSURANCE")) / 2
)

CHURCH_TAX = 0 if os.getenv("CHURCH_TAX") is None else float(os.getenv("CHURCH_TAX"))
