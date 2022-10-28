from netto.config import EXTRA_HEALTH_INSURANCE


tax_curve = {
    2022: {
        0: {"step": 10347, "rate": 0.14},
        1: {"step": 14926, "rate": 0.2397},
        2: {"step": 58596, "rate": 0.42},
        3: {"step": 277826, "rate": 0.45},
    }
}


social_security_curve = {
    2022: {
        "pension": {"limit": 84600, "rate": 0.093},
        "unemployment": {"limit": 84600, "rate": 0.012},
        "health": {"limit": 58050, "rate": 0.073, "extra": EXTRA_HEALTH_INSURANCE},
        "nursing": {"limit": 58050, "rate": 0.01525, "extra": 0.0035},
    }
}


correction_factor_pensions = {
    2018: 0.72,
    2019: 0.76,
    2020: 0.8,
    2021: 0.84,
    2022: 0.88,
    2023: 0.92,
    2024: 0.96,
    2025: 1.00,
}
