import os
import unittest
from unittest.mock import patch

from netto.config import TaxConfig, load_config_from_env, reset_default_config


class TestConfig(unittest.TestCase):
    def tearDown(self):
        # Reset default config after each test
        reset_default_config()

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

    @patch.dict(
        os.environ,
        {
            "YEAR": "2023",
            "HAS_CHILDREN": "True",
            "IS_MARRIED": "True",
            "EXTRA_HEALTH_INSURANCE": "0.015",
            "CHURCH_TAX": "0.1",
        },
    )
    def test_load_config_from_env_valid(self):
        """Test loading configuration from environment variables"""
        config = load_config_from_env()
        self.assertEqual(config.year, 2023)
        self.assertTrue(config.has_children)
        self.assertTrue(config.is_married)
        self.assertEqual(config.extra_health_insurance, 0.015)
        self.assertEqual(config.church_tax, 0.1)

    @patch.dict(
        os.environ,
        {
            "YEAR": "invalid",
            "HAS_CHILDREN": "invalid",
            "IS_MARRIED": "invalid",
            "EXTRA_HEALTH_INSURANCE": "invalid",
            "CHURCH_TAX": "invalid",
        },
    )
    def test_load_config_from_env_invalid(self):
        """Test that invalid environment variables fall back to defaults"""
        config = load_config_from_env()
        self.assertEqual(config.year, 2022)
        self.assertFalse(config.has_children)
        self.assertFalse(config.is_married)
        self.assertEqual(config.extra_health_insurance, 0.014)
        self.assertEqual(config.church_tax, 0.09)

    @patch.dict(os.environ, {}, clear=True)
    def test_load_config_from_env_empty(self):
        """Test that missing environment variables use defaults"""
        config = load_config_from_env()
        self.assertEqual(config.year, 2022)
        self.assertFalse(config.has_children)
        self.assertFalse(config.is_married)
        self.assertEqual(config.extra_health_insurance, 0.014)
        self.assertEqual(config.church_tax, 0.09)
