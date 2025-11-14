"""
Tax and social security constants.

This module provides access to tax curves, social security rates,
solidarity tax parameters, and pension correction factors for
various tax years.

Data is now loaded from JSON files in the data/ directory and
validated using Pydantic models. See data_loader.py for details.
"""

from netto.data_loader import (
    load_all_social_security,
    load_all_tax_curves,
    load_pension_correction_factors,
    load_soli,
)

# Load all data from JSON files
__tax_curve = load_all_tax_curves()
__social_security_curve = load_all_social_security()
__soli_curve = load_soli()
__correction_factor_pensions = load_pension_correction_factors()
