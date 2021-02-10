import time
import unittest

import httpie_ovh_auth


class TestSignature(unittest.TestCase):

    def test_signature(self):
        timestamp = time.mktime(time.strptime('2020-02-10', '%Y-%m-%d'))
        def sign(method):
            return httpie_ovh_auth.sign('secret_key', 'consumer_key', method,
                               'https://url.com/path', '{"json": "content"}',
                               timestamp)
        signature1 = sign('get')
        signature2 = sign('GET')
        # check signature
        assert signature1 == "7ec7ff1bfa04620f934e2b3d0fbd947e653acb1a", \
               "signature differs from expected value"
        # check method serialization
        assert signature1 == signature2, \
               "signature must not be sensible to method case"
        return
