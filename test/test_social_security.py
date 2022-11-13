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


