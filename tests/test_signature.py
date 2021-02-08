import unittest

import httpie_ovh_auth


class TestSignature(unittest.TestCase):

    def test_signature(self):
        httpie_ovh_auth.OvhAuthPlugin()
        return
