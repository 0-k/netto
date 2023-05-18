import importlib
import os
import unittest
from unittest.mock import patch

import netto.config as config


class TestConfig(unittest.TestCase):
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
    def test_env_variables_set_correctly(self):
        importlib.reload(config)
        config.load_config()
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
    def test_invalid_env_variables(self):
        importlib.reload(config)
        config.load_config()
        self.assertEqual(config.year, 2022)
        self.assertFalse(config.has_children)
        self.assertFalse(config.is_married)
        self.assertEqual(config.extra_health_insurance, 0.014)
        self.assertEqual(config.church_tax, 0.09)
