import unittest
import netto.social_security as social_security
import netto.config as config


class TestSocialSecurity(unittest.TestCase):
    def setUp(self):
        config.EXTRA_HEALTH_INSURANCE = 0.014
        config.CHURCH_TAX = 0.09
        config.HAS_CHILDREN = False

    def tearDown(self):
        pass

    def test_get_rate_pension(self):
        self.assertEqual(social_security.get_rate_pension(0), 0)
        self.assertEqual(social_security.get_rate_pension(10000), 0.093)
        self.assertEqual(social_security.get_rate_pension(84600), 0.093)
        self.assertEqual(social_security.get_rate_pension(84601), 0)
        self.assertEqual(social_security.get_rate_pension(100000), 0)

    def test_get_rate_health(self):
        self.assertEqual(social_security.get_rate_health(0), 0)
        self.assertEqual(social_security.get_rate_health(10000), 0.08)
        self.assertEqual(social_security.get_rate_health(58050), 0.08)
        self.assertEqual(social_security.get_rate_health(58051), 0)
        self.assertEqual(social_security.get_rate_health(100000), 0)

    def test_calc_insurance_pension(self):
        self.assertEqual(social_security.calc_insurance_pension(0), 0)
        self.assertEqual(social_security.calc_insurance_pension(10000), 0.093 * 10000)
        self.assertEqual(social_security.calc_insurance_pension(84600), 0.093 * 84600)
        self.assertEqual(social_security.calc_insurance_pension(84601), 0.093 * 84600)
        self.assertEqual(social_security.calc_insurance_pension(100000), 0.093 * 84600)

    def test_calc_insurance_health(self):
        self.assertEqual(social_security.calc_insurance_health(0), 0)
        self.assertEqual(social_security.calc_insurance_health(10000), 0.08 * 10000)
        self.assertEqual(social_security.calc_insurance_health(58050), 0.08 * 58050)
        self.assertEqual(social_security.calc_insurance_health(58051), 0.08 * 58050)
        self.assertEqual(social_security.calc_insurance_health(100000), 0.08 * 58050)

    def test_calc_deductable_social_security(self):
        self.assertEqual(social_security.calc_deductable_social_security(0), 0)
        self.assertEqual(
            social_security.calc_deductable_social_security(30000),
            2456 + 2310 + 563,  # https://www.lohn-info.de/vorsorgepauschale.html
        )

    def test_sameness_of_calc_social_security(self):
        for salary in range(0, 100001, 10000):
            self.assertEqual(
                social_security.calc_social_security(salary),
                social_security.calc_social_security_by_integration(salary),
            )

    def test_sameness_of_calc_social_security_different_config(self):
        config.EXTRA_HEALTH_INSURANCE = 0.015
        config.HAS_CHILDREN = True
        for salary in range(0, 100001, 10000):
            self.assertEqual(
                social_security.calc_social_security(salary),
                social_security.calc_social_security_by_integration(salary),
            )

    def test_get_rate_health_different_config(self):
        config.EXTRA_HEALTH_INSURANCE = 0.015
        self.assertEqual(social_security.get_rate_health(0), 0)
        self.assertAlmostEqual(social_security.get_rate_health(10000), 0.0805)
        self.assertAlmostEqual(social_security.get_rate_health(58050), 0.0805)
        self.assertEqual(social_security.get_rate_health(58051), 0)
        self.assertEqual(social_security.get_rate_health(100000), 0)

    def test_get_rate_nursing(self):
        config.HAS_CHILDREN = False
        self.assertEqual(social_security.get_rate_nursing(0), 0)
        self.assertEqual(social_security.get_rate_nursing(10000), 0.01875)
        self.assertEqual(social_security.get_rate_nursing(58050), 0.01875)
        self.assertEqual(social_security.get_rate_nursing(58051), 0)
        self.assertEqual(social_security.get_rate_nursing(100000), 0)

    def test_get_rate_nursing_different_config(self):
        config.HAS_CHILDREN = True
        self.assertEqual(social_security.get_rate_nursing(0), 0)
        self.assertEqual(social_security.get_rate_nursing(10000), 0.01525)
        self.assertEqual(social_security.get_rate_nursing(58050), 0.01525)
        self.assertEqual(social_security.get_rate_nursing(58051), 0)
        self.assertEqual(social_security.get_rate_nursing(100000), 0)
