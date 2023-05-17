import unittest

import netto.config as config
import netto.taxes_income as taxes_income


class TestTaxesIncome(unittest.TestCase):
    def setUp(self):
        config.extra_health_insurance = 0.014
        config.church_tax = 0.09
        config.has_children = False

    def tearDown(self):
        pass

    def test_valid_get_marginal_tax_rate(self):
        self.assertEqual(taxes_income.get_marginal_tax_rate(-1000), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(0), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10346), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10347), 0.14)
        self.assertEqual(taxes_income.get_marginal_tax_rate(14926), 0.2397)
        self.assertEqual(taxes_income.get_marginal_tax_rate(58596), 0.42)
        self.assertEqual(taxes_income.get_marginal_tax_rate(58597), 0.42)
        self.assertEqual(taxes_income.get_marginal_tax_rate(100000), 0.42)
        self.assertEqual(taxes_income.get_marginal_tax_rate(277826), 0.45)
        self.assertEqual(taxes_income.get_marginal_tax_rate(277827), 0.45)

    def test_valid_get_marginal_tax_rate_married(self):
        config.is_married = True
        self.assertEqual(taxes_income.get_marginal_tax_rate(10346), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10347), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10346 * 2), 0)
        self.assertEqual(taxes_income.get_marginal_tax_rate(10347 * 2), 0.14)
        config.is_married = False

    def test_sameness_of_calc_income_tax_methods(self):
        self.assertAlmostEqual(
            taxes_income.calc_income_tax(12000),
            taxes_income.calc_income_tax_by_integration(12000),
            delta=0.1,
        )
        for taxable_income in range(0, 100001, 10000):
            self.assertAlmostEqual(
                taxes_income.calc_income_tax(taxable_income),
                taxes_income.calc_income_tax_by_integration(taxable_income),
                delta=0.1,
            )
        self.assertAlmostEqual(
            taxes_income.calc_income_tax(300000),
            taxes_income.calc_income_tax_by_integration(300000),
            delta=0.1,
        )
