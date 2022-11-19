import unittest
import netto.taxes_income as taxes_income
import netto.config as config


class TestTaxesIncome(unittest.TestCase):
    def setUp(self):
        config.EXTRA_HEALTH_INSURANCE = 0.014
        config.CHURCH_TAX = 0.09
        config.HAS_CHILDREN = False

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

    def test_sameness_of_calc_income_tax_methods(self):
        for taxable_income in range(0, 100001, 10000):
            self.assertAlmostEqual(
                taxes_income.calc_income_tax(taxable_income),
                taxes_income.calc_income_tax_by_integration(taxable_income),
                delta=0.1,
            )
