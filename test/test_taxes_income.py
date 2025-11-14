import unittest

from netto.config import TaxConfig
import netto.taxes_income as taxes_income


class TestTaxesIncome(unittest.TestCase):
    def setUp(self):
        # Create default config for tests
        self.default_config = TaxConfig(
            extra_health_insurance=0.014,
            church_tax=0.09,
            has_children=False
        )

    def tearDown(self):
        pass

    def test_valid_get_marginal_tax_rate(self):
        self.assertEqual(taxes_income.get_marginal_tax_rate(-1000, self.default_config), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(0, self.default_config), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10346, self.default_config), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10347, self.default_config), 0.14)
        self.assertEqual(taxes_income.get_marginal_tax_rate(14926, self.default_config), 0.2397)
        self.assertEqual(taxes_income.get_marginal_tax_rate(58596, self.default_config), 0.42)
        self.assertEqual(taxes_income.get_marginal_tax_rate(58597, self.default_config), 0.42)
        self.assertEqual(taxes_income.get_marginal_tax_rate(100000, self.default_config), 0.42)
        self.assertEqual(taxes_income.get_marginal_tax_rate(277826, self.default_config), 0.45)
        self.assertEqual(taxes_income.get_marginal_tax_rate(277827, self.default_config), 0.45)

    def test_valid_get_marginal_tax_rate_married(self):
        config = TaxConfig(is_married=True)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10346, config), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10347, config), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10346 * 2, config), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10347 * 2, config), 0.14)

    def test_sameness_of_calc_income_tax_methods(self):
        self.assertAlmostEqual(
            taxes_income.calc_income_tax(12000, self.default_config),
            taxes_income.calc_income_tax_by_integration(12000, self.default_config),
            delta=0.1,
        )
        for taxable_income in range(0, 100001, 10000):
            self.assertAlmostEqual(
                taxes_income.calc_income_tax(taxable_income, self.default_config),
                taxes_income.calc_income_tax_by_integration(taxable_income, self.default_config),
                delta=0.1,
            )
        self.assertAlmostEqual(
            taxes_income.calc_income_tax(300000, self.default_config),
            taxes_income.calc_income_tax_by_integration(300000, self.default_config),
            delta=0.1,
        )
