import unittest
import netto.taxes_other as taxes_other


class TestTaxesOther(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_calc_soli(self):
        self.assertEqual(taxes_other.calc_soli(-1000), 0)
        self.assertEqual(taxes_other.calc_soli(0), 0)
        self.assertEqual(taxes_other.calc_soli(16956), 0)
        self.assertAlmostEqual(taxes_other.calc_soli(16957), 0.119, places=1)
        self.assertAlmostEqual(taxes_other.calc_soli(17514.96), 66.48, places=1)
        self.assertAlmostEqual(taxes_other.calc_soli(26913.96), 1185.0, places=1)
        self.assertEqual(taxes_other.calc_soli(100000), 5500)

    def test_valid_calc_church_tax(self):
        self.assertEqual(taxes_other.calc_church_tax(-1000), 0)
        self.assertEqual(taxes_other.calc_church_tax(0), 0)
        self.assertEqual(taxes_other.calc_church_tax(10000), 900)
