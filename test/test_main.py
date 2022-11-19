import unittest
import netto.main as main
import netto.config as config


class TestMain(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_for_valid_main(self):
        self.assertEqual(main.calc_netto(0), 0)
        self.assertAlmostEqual(main.calc_netto(30000)/12, 20554.38/12, 0)
        self.assertAlmostEqual(main.calc_netto(60000)/12, 35796.68/12, 0)
        self.assertAlmostEqual(main.calc_netto(90000)/12, 49956.92/12, 0)
        self.assertAlmostEqual(main.calc_netto(120000)/12, 64965.08/12, 0)

        config.EXTRA_HEALTH_INSURANCE = 0.015
        config.CHURCH_TAX = 0.0
        config.HAS_CHILDREN = True
        self.assertAlmostEqual(main.calc_netto(30000)/12, 20894.58/12, 0)
        self.assertAlmostEqual(main.calc_netto(60000)/12, 36909.71/12, 0)
        self.assertAlmostEqual(main.calc_netto(90000)/12, 52091.39/12, 0)
        self.assertAlmostEqual(main.calc_netto(120000)/12, 68238.23/12, 0)


