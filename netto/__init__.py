from netto.config import TaxConfig
from netto.main import calc_inverse_netto, calc_netto
from netto.social_security import (
    calc_deductible_social_security,
    calc_insurance_health,
    calc_insurance_nursing,
    calc_insurance_pension,
    calc_insurance_unemployment,
    calc_social_security,
    calc_social_security_by_integration,
    get_rate_health,
    get_rate_nursing,
    get_rate_pension,
    get_rate_unemployment,
)
from netto.taxes_income import (
    calc_income_tax,
    calc_income_tax_by_integration,
    calc_taxable_income,
    get_marginal_tax_rate,
)
from netto.taxes_other import calc_church_tax, calc_soli

__all__ = [
    # Main API
    "calc_netto",
    "calc_inverse_netto",
    # Configuration
    "TaxConfig",
    # Social Security
    "calc_social_security",
    "calc_deductible_social_security",
    "calc_social_security_by_integration",
    "calc_insurance_pension",
    "calc_insurance_health",
    "calc_insurance_nursing",
    "calc_insurance_unemployment",
    "get_rate_pension",
    "get_rate_health",
    "get_rate_nursing",
    "get_rate_unemployment",
    # Income Tax
    "calc_income_tax",
    "calc_income_tax_by_integration",
    "calc_taxable_income",
    "get_marginal_tax_rate",
    # Other Taxes
    "calc_soli",
    "calc_church_tax",
]
