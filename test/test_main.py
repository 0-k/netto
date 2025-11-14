import unittest
from io import StringIO
from unittest.mock import patch

from netto.config import TaxConfig
import netto.main as main


class TestMain(unittest.TestCase):
    def setUp(self):
        # Create default config for tests
        self.default_config = TaxConfig(
            extra_health_insurance=0.014,
            church_tax=0.09,
            has_children=False
        )

    def tearDown(self):
        pass

    def test_for_valid_main(self):
        self.assertEqual(main.calc_netto(0, config=self.default_config), 0)
        self.assertAlmostEqual(main.calc_netto(30000, config=self.default_config), 20554.38, delta=1)
        self.assertAlmostEqual(main.calc_netto(60000, config=self.default_config), 35796.68, delta=1)
        self.assertAlmostEqual(main.calc_netto(90000, config=self.default_config), 49956.92, delta=1)
        self.assertAlmostEqual(main.calc_netto(120000, config=self.default_config), 64965.08, delta=1)

    def test_for_valid_main_second_config(self):
        config = TaxConfig(
            extra_health_insurance=0.015,
            church_tax=0.0,
            has_children=True
        )
        self.assertAlmostEqual(main.calc_netto(30000, config=config), 20894.58, delta=1)
        self.assertAlmostEqual(main.calc_netto(60000, config=config), 36909.71, delta=1)
        self.assertAlmostEqual(main.calc_netto(90000, config=config), 52091.39, delta=1)
        self.assertAlmostEqual(main.calc_netto(120000, config=config), 68238.23, delta=1)

    def test_for_valid_inverse_netto(self):
        config = TaxConfig(
            extra_health_insurance=0.015,
            church_tax=0.0,
            has_children=True
        )
        self.assertEqual(main.calc_inverse_netto(main.calc_netto(10000, config=config), config=config), 10000)
        self.assertAlmostEqual(main.calc_inverse_netto(20894.58, config=config), 30000, delta=1)
        self.assertAlmostEqual(main.calc_inverse_netto(36909.71, config=config), 60000, delta=1)
        self.assertAlmostEqual(main.calc_inverse_netto(52091.39, config=config), 90000, delta=1)
        self.assertAlmostEqual(main.calc_inverse_netto(68238.23, config=config), 120000, delta=1)

    @patch("sys.stdout", new_callable=StringIO)
    def test_verbose_print(self, mock_stdout):
        main.calc_netto(0, verbose=True, config=self.default_config)
        actual_output = mock_stdout.getvalue().strip()
        expected_output = (
            "Yearly Evaluation:\n"
            + f"Income Tax:      {0.0:>12}\n"
            + f"Soli:            {0.0:>12}\n"
            + f"Church Tax:      {0.0:>12}\n"
            + f"Social Security: {0.0:>12}"
        )
        self.assertEqual(actual_output, expected_output)
