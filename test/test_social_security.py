import unittest
import netto.social_security as social_security


class TestSocialSecurity(unittest.TestCase):
    def setUp(self):
        pass

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
        self.assertEqual(social_security.calc_insurance_health(84600), 0.08 * 58050)
        self.assertEqual(social_security.calc_insurance_health(84601), 0.08 * 58050)
        self.assertEqual(social_security.calc_insurance_health(100000), 0.08 * 58050)

    def test_calc_deductable_social_security(self):
        self.assertEqual(social_security.calc_deductable_social_security(0), 0)
        self.assertEqual(
            social_security.calc_deductable_social_security(30000),
            2455.20 + 2310 + 562.50,
        )

    def test_sameness_of_calc_social_securitx(self):
        for salary in range(0, 100001, 10000):
            self.assertEqual(
                social_security.calc_social_security(salary),
                social_security.calc_social_security_by_integration(salary),
            )
