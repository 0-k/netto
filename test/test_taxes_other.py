import unittest

from netto.config import TaxConfig
import netto.taxes_other as taxes_other


class TestTaxesOther(unittest.TestCase):
    def setUp(self):
        # Create default config for tests
        self.default_config = TaxConfig(
            extra_health_insurance=0.014,
            church_tax=0.09,
            has_children=False
        )

    def tearDown(self):
        pass

    def test_valid_calc_soli(self):
        self.assertEqual(taxes_other.calc_soli(-1000, self.default_config), 0)
        self.assertEqual(taxes_other.calc_soli(0, self.default_config), 0)
        self.assertEqual(taxes_other.calc_soli(16956, self.default_config), 0)
        self.assertAlmostEqual(taxes_other.calc_soli(16957, self.default_config), 0.119, delta=0.1)
        self.assertAlmostEqual(taxes_other.calc_soli(17514.96, self.default_config), 66.48, delta=0.1)
        self.assertAlmostEqual(taxes_other.calc_soli(26913.96, self.default_config), 1185.0, delta=0.1)
        self.assertEqual(taxes_other.calc_soli(100000, self.default_config), 5500)

    def test_valid_calc_church_tax(self):
        self.assertEqual(taxes_other.calc_church_tax(-1000, self.default_config), 0)
        self.assertEqual(taxes_other.calc_church_tax(0, self.default_config), 0)
        self.assertEqual(taxes_other.calc_church_tax(10000, self.default_config), 900)
