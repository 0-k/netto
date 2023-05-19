import unittest
from io import StringIO
from unittest.mock import patch

import netto.config as config
import netto.main as main


class TestMain(unittest.TestCase):
    def setUp(self):
        config.extra_health_insurance = 0.014
        config.church_tax = 0.09
        config.has_children = False

    def tearDown(self):
        pass

    def test_for_valid_main(self):
        self.assertEqual(main.calc_netto(0), 0)
        self.assertAlmostEqual(main.calc_netto(30000), 20554.38, delta=1)
        self.assertAlmostEqual(main.calc_netto(60000), 35796.68, delta=1)
        self.assertAlmostEqual(main.calc_netto(90000), 49956.92, delta=1)
        self.assertAlmostEqual(main.calc_netto(120000), 64965.08, delta=1)

    def test_for_valid_main_second_config(self):
        config.extra_health_insurance = 0.015
        config.church_tax = 0.0
        config.has_children = True
        self.assertAlmostEqual(main.calc_netto(30000), 20894.58, delta=1)
        self.assertAlmostEqual(main.calc_netto(60000), 36909.71, delta=1)
        self.assertAlmostEqual(main.calc_netto(90000), 52091.39, delta=1)
        self.assertAlmostEqual(main.calc_netto(120000), 68238.23, delta=1)

    def test_for_valid_inverse_netto(self):
        config.extra_health_insurance = 0.015
        config.church_tax = 0.0
        config.has_children = True
        self.assertEqual(main.calc_inverse_netto(main.calc_netto(10000)), 10000)
        self.assertAlmostEqual(main.calc_inverse_netto(20894.58), 30000, delta=1)
        self.assertAlmostEqual(main.calc_inverse_netto(36909.71), 60000, delta=1)
        self.assertAlmostEqual(main.calc_inverse_netto(52091.39), 90000, delta=1)
        self.assertAlmostEqual(main.calc_inverse_netto(68238.23), 120000, delta=1)

    @patch("sys.stdout", new_callable=StringIO)
    def test_verbose_print(self, mock_stdout):
        main.calc_netto(0, verbose=True)
        actual_output = mock_stdout.getvalue().strip()
        expected_output = (
            "Yearly Evaluation:\n"
            + f"Income Tax:      {0.0:>12}\n"
            + f"Soli:            {0.0:>12}\n"
            + f"Church Tax:      {0.0:>12}\n"
            + f"Social Security: {0.0:>12}"
        )
        self.assertEqual(actual_output, expected_output)
