import unittest
import netto.main as main
import netto.config as config


class TestMain(unittest.TestCase):
    def setUp(self):
        config.EXTRA_HEALTH_INSURANCE = 0.014
        config.CHURCH_TAX = 0.09
        config.HAS_CHILDREN = False

    def tearDown(self):
        pass

    def test_for_valid_main(self):
        self.assertEqual(main.calc_netto(0), 0)
        self.assertAlmostEqual(main.calc_netto(30000), 20554.38, delta=1)
        self.assertAlmostEqual(main.calc_netto(60000), 35796.68, delta=1)
        self.assertAlmostEqual(main.calc_netto(90000), 49956.92, delta=1)
        self.assertAlmostEqual(main.calc_netto(120000), 64965.08, delta=1)

    def test_for_valid_main_second_config(self):
        config.EXTRA_HEALTH_INSURANCE = 0.015
        config.CHURCH_TAX = 0.0
        config.HAS_CHILDREN = True
        self.assertAlmostEqual(main.calc_netto(30000), 20894.58, delta=1)
        self.assertAlmostEqual(main.calc_netto(60000), 36909.71, delta=1)
        self.assertAlmostEqual(main.calc_netto(90000), 52091.39, delta=1)
        self.assertAlmostEqual(main.calc_netto(120000), 68238.23, delta=1)
