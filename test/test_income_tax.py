import unittest
import netto.income_tax as income_tax


class TestMain(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_get_marginal_tax_rate(self):
        self.assertEqual(income_tax.get_marginal_tax_rate(-1000), 0)
        self.assertEqual(income_tax.get_marginal_tax_rate(0), 0)
        self.assertEqual(income_tax.get_marginal_tax_rate(10346), 0)
        self.assertEqual(income_tax.get_marginal_tax_rate(10347), 0.14)
        self.assertEqual(income_tax.get_marginal_tax_rate(14926), 0.2397)
        self.assertEqual(income_tax.get_marginal_tax_rate(58596), 0.42)
        self.assertEqual(income_tax.get_marginal_tax_rate(58597), 0.42)
        self.assertEqual(income_tax.get_marginal_tax_rate(100000), 0.42)
        self.assertEqual(income_tax.get_marginal_tax_rate(277826), 0.45)
        self.assertEqual(income_tax.get_marginal_tax_rate(277827), 0.45)

