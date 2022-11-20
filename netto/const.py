tax_curve = {
    2018: {
        0: {"step": 9000, "rate": 0.14},
        1: {"step": 13996, "rate": 0.2397, "const": [997.8, 1400]},
        2: {"step": 54949, "rate": 0.42, "const": [220.13, 2397, 948.49]},
        3: {"step": 260533, "rate": 0.45, "const": [8621.75, 16437.7]},
    },
    2019: {
        0: {"step": 9168, "rate": 0.14},
        1: {"step": 14254, "rate": 0.2397, "const": [980.14, 1400]},
        2: {"step": 55960, "rate": 0.42, "const": [216.16, 2397, 965.58]},
        3: {"step": 265327, "rate": 0.45, "const": [8780.9, 16740.68]},
    },
    2020: {
        0: {"step": 9408, "rate": 0.14},
        1: {"step": 14532, "rate": 0.2397, "const": [972.87, 1400]},
        2: {"step": 57051, "rate": 0.42, "const": [212.02, 2397, 972.79]},
        3: {"step": 270501, "rate": 0.45, "const": [8963.74, 17078.74]},
    },
    2021: {
        0: {"step": 9744, "rate": 0.14},
        1: {"step": 14753, "rate": 0.2397, "const": [995.21, 1400]},
        2: {"step": 57918, "rate": 0.42, "const": [208.85, 2397, 950.96]},
        3: {"step": 274613, "rate": 0.45, "const": [9136.63, 17374.99]},
    },
    2022: {
        0: {"step": 10347, "rate": 0.14},
        1: {"step": 14926, "rate": 0.2397, "const": [1088.67, 1400]},
        2: {"step": 58596, "rate": 0.42, "const": [206.43, 2397, 869.32]},
        3: {"step": 277826, "rate": 0.45, "const": [9336.45, 17671.20]},
    },
    2023: {
        0: {"step": 10633, "rate": 0.14},
        1: {
            "step": 15786,
            "rate": 0.2397,
            "const": [NotImplementedError, NotImplementedError],
        },
        2: {
            "step": 61971,
            "rate": 0.42,
            "const": [NotImplementedError, NotImplementedError, NotImplementedError],
        },
        3: {
            "step": 277826,
            "rate": 0.45,
            "const": [NotImplementedError, NotImplementedError],
        },
    },
    2024: {
        0: {"step": 10933, "rate": 0.14},
        1: {
            "step": 16179,
            "rate": 0.2397,
            "const": [NotImplementedError, NotImplementedError],
        },
        2: {
            "step": 63514,
            "rate": 0.42,
            "const": [NotImplementedError, NotImplementedError, NotImplementedError],
        },
        3: {
            "step": 277826,
            "rate": 0.45,
            "const": [NotImplementedError, NotImplementedError],
        },
    },
    2025: NotImplementedError,
}


social_security_curve = {
    2018: {
        "pension": {"limit": 78000, "rate": 0.093},
        "unemployment": {"limit": 78000, "rate": 0.015},
        "health": {"limit": 53100, "rate": 0.073},
        "nursing": {"limit": 53100, "rate": 0.01275, "extra": 0.0025},
    },
    2019: {
        "pension": {"limit": 80400, "rate": 0.093},
        "unemployment": {"limit": 80400, "rate": 0.0125},
        "health": {"limit": 54450, "rate": 0.073},
        "nursing": {"limit": 54450, "rate": 0.01525, "extra": 0.0025},
    },
    2020: {
        "pension": {"limit": 82800, "rate": 0.093},
        "unemployment": {"limit": 82800, "rate": 0.012},
        "health": {"limit": 56250, "rate": 0.073},
        "nursing": {"limit": 56250, "rate": 0.01525, "extra": 0.0025},
    },
    2021: {
        "pension": {"limit": 85200, "rate": 0.093},
        "unemployment": {"limit": 85200, "rate": 0.012},
        "health": {"limit": 58050, "rate": 0.073},
        "nursing": {"limit": 58050, "rate": 0.01525, "extra": 0.0025},
    },
    2022: {
        "pension": {"limit": 84600, "rate": 0.093},
        "unemployment": {"limit": 84600, "rate": 0.012},
        "health": {"limit": 58050, "rate": 0.073},
        "nursing": {"limit": 58050, "rate": 0.01525, "extra": 0.0035},
    },
    2023: {
        "pension": {"limit": 87600, "rate": 0.093},
        "unemployment": {"limit": 87600, "rate": 0.012},
        "health": {"limit": 59850, "rate": 0.073},
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
