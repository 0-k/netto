tax_curve = {
    2018: NotImplementedError,
    2019: NotImplementedError,
    2020: {
        0: {"step": 10347, "rate": 0.14},
        1: {"step": 14926, "rate": 0.2397, "const": [1088.67, 1400]},
        2: {"step": 58596, "rate": 0.42, "const": [206.43, 2397, 869.32]},
        3: {"step": 277826, "rate": 0.45, "const": [9336.45, 17671.20]},
    },
    2021: {
        0: {"step": 9744, "rate": 0.14},
        1: {"step": 14926, "rate": 0.2397, "const": [1088.67, 1400]},
        2: {"step": 58596, "rate": 0.42, "const": [206.43, 2397, 869.32]},
        3: {"step": 277826, "rate": 0.45, "const": [9336.45, 17671.20]},
    },
    2022: {
        0: {"step": 10347, "rate": 0.14},
        1: {"step": 14926, "rate": 0.2397, "const": [1088.67, 1400]},
        2: {"step": 58596, "rate": 0.42, "const": [206.43, 2397, 869.32]},
        3: {"step": 277826, "rate": 0.45, "const": [9336.45, 17671.20]},
    },
    2023: {
        0: {"step": 10633, "rate": 0.14},
        1: {"step": 15786, "rate": 0.2397, "const": NotImplementedError},
        2: {"step": 61971, "rate": 0.42, "const": NotImplementedError},
        3: {"step": 277826, "rate": 0.45, "const": NotImplementedError},
    },
    2024: {
        0: {"step": 10933, "rate": 0.14},
        1: {"step": 16179, "rate": 0.2397, "const": NotImplementedError},
        2: {"step": 63514, "rate": 0.42, "const": NotImplementedError},
        3: {"step": 277826, "rate": 0.45, "const": NotImplementedError},
    },
    2025: NotImplementedError,
}


social_security_curve = {
    2018: NotImplementedError,
    2019: NotImplementedError,
    2020: {
        "pension": {"limit": 82800, "rate": 0.093},
        "unemployment": {"limit": 82800, "rate": 0.012},
        "health": {
            "limit": 56250,
            "rate": 0.073,
        },
        "nursing": {"limit": 56250, "rate": 0.01525, "extra": 0.0025},
    },
    2021: {
        "pension": {"limit": 85200, "rate": 0.093},
        "unemployment": {"limit": 85200, "rate": 0.012},
        "health": {
            "limit": 58050,
            "rate": 0.073,
        },
        "nursing": {"limit": 58050, "rate": 0.01525, "extra": 0.0025},
    },
    2022: {
        "pension": {"limit": 84600, "rate": 0.093},
        "unemployment": {"limit": 84600, "rate": 0.012},
        "health": {
            "limit": 58050,
            "rate": 0.073,
        },
        "nursing": {"limit": 58050, "rate": 0.01525, "extra": 0.0035},
    },
    2023: {
        "pension": {"limit": 87600, "rate": 0.093},
        "unemployment": {"limit": 87600, "rate": 0.012},
        "health": {
            "limit": 59850,
            "rate": 0.073,
        },
        "nursing": {"limit": 59850, "rate": 0.01525, "extra": 0.0035},
    },
    2024: NotImplementedError,
    2025: NotImplementedError,
}


soli_curve = {
    2018: {"start_taxable_income": 972, "start_fraction": 0.2, "end_rate": 0.055},
    2019: {"start_taxable_income": 972, "start_fraction": 0.2, "end_rate": 0.055},
    2020: {"start_taxable_income": 972, "start_fraction": 0.2, "end_rate": 0.055},
    2021: {"start_taxable_income": 16956, "start_fraction": 0.119, "end_rate": 0.055},
    2022: {"start_taxable_income": 16956, "start_fraction": 0.119, "end_rate": 0.055},
    2023: {"start_taxable_income": 17543, "start_fraction": 0.119, "end_rate": 0.055},
    2024: {"start_taxable_income": 18130, "start_fraction": 0.119, "end_rate": 0.055},
    2025: NotImplementedError,
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
