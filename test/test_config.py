import unittest

from netto.config import TaxConfig


class TestConfig(unittest.TestCase):
    def test_taxconfig_defaults(self):
        """Test that TaxConfig uses correct default values"""
        config = TaxConfig()
        self.assertEqual(config.year, 2022)
        self.assertFalse(config.has_children)
        self.assertFalse(config.is_married)
        self.assertEqual(config.extra_health_insurance, 0.014)
        self.assertEqual(config.church_tax, 0.09)

    def test_taxconfig_custom_values(self):
        """Test creating TaxConfig with custom values"""
        config = TaxConfig(
            year=2025,
            has_children=True,
            is_married=True,
            extra_health_insurance=0.02,
            church_tax=0.08
        )
        self.assertEqual(config.year, 2025)
        self.assertTrue(config.has_children)
        self.assertTrue(config.is_married)
        self.assertEqual(config.extra_health_insurance, 0.02)
        self.assertEqual(config.church_tax, 0.08)

    def test_taxconfig_validation_year_range(self):
        """Test that year validation works"""
        with self.assertRaises(ValueError):
            TaxConfig(year=2017)  # Too early
        with self.assertRaises(ValueError):
            TaxConfig(year=2026)  # Too late

    def test_taxconfig_validation_negative_rates(self):
        """Test that negative rates are rejected"""
        with self.assertRaises(ValueError):
            TaxConfig(extra_health_insurance=-0.01)
        with self.assertRaises(ValueError):
            TaxConfig(church_tax=-0.01)

    def test_taxconfig_validation_type_errors(self):
        """Test that type validation works"""
        with self.assertRaises(TypeError):
            TaxConfig(year="2022")  # String instead of int
        with self.assertRaises(TypeError):
            TaxConfig(has_children="True")  # String instead of bool
        with self.assertRaises(TypeError):
            TaxConfig(is_married=1)  # Int instead of bool
