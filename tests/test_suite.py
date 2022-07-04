import calendar
import time
import unittest
from unittest.mock import call
from unittest.mock import patch
from unittest.mock import sentinel

import httpie_ovh_auth
import httpie.models


class TestSuite(unittest.TestCase):
    def test_signature(self):
        """Check signature generation."""
        # time_o without any timezone info
        time_o = time.strptime("2020-02-10 +0000", "%Y-%m-%d %z")
        # time_o interpreted as UTC to provide epoch
        timestamp = calendar.timegm(time_o)

        def sign(method):
            return httpie_ovh_auth.sign(
                "secret_key",
                "consumer_key",
                method,
                "https://url.com/path",
                '{"json": "content"}',
                timestamp,
            )

        signature1 = sign("get")
        signature2 = sign("GET")
        # check signature
        assert (
            signature1 == "cfcd791f25a9786eda88926c7a7ad68580e6bb45"
        ), "signature differs from expected value"
        # check method serialization
        assert signature1 == signature2, "signature must not be sensible to method case"
        return

    @patch("os.getenv")
    def test_env(self, GetEnv):
        """Check that plugin init load configuration from environment."""
        GetEnv.return_value = None
        p = httpie_ovh_auth.OvhAuthPlugin()
        GetEnv.assert_has_calls(
            [
                call("OVH_CLIENT_ID", None),
                call("OVH_CLIENT_SECRET", None),
                call("OVH_CONSUMER_KEY", None),
            ],
            any_order=True,
        )

    @patch("os.getenv")
    def test_env_empty(self, GetEnv):
        """Check that an exception is raised if environment variables
        are empty. Check that message provides environment variables
        names."""
        GetEnv.return_value = None
        p = httpie_ovh_auth.OvhAuthPlugin()
        with (self.assertRaises(httpie_ovh_auth.OvhAuthException)) as e:
            p.get_auth()
            assert "OVH_CLIENT_ID" in str(e.exception)
            assert "OVH_CLIENT_SECRET" in str(e.exception)
            assert "OVH_CONSUMER_KEY" in str(e.exception)

    @patch("httpie_ovh_auth.OvhAuth")
    @patch("os.getenv")
    def test_env_not_empty(self, GetEnv, OvhAuth):
        """Check that OvhAuth is correctly built if credentials are
        present."""

        def side_effect(arg1, arg2):
            return getattr(sentinel, arg1)

        GetEnv.side_effect = side_effect
        p = httpie_ovh_auth.OvhAuthPlugin()
        p.get_auth()
        OvhAuth.assert_called_once_with(
            getattr(sentinel, "OVH_CLIENT_ID"),
            getattr(sentinel, "OVH_CLIENT_SECRET"),
            getattr(sentinel, "OVH_CONSUMER_KEY"),
        )

    @patch("time.time", return_value=12345)
    @patch("httpie_ovh_auth.sign", return_value="XX_SIGN_XX")
    @patch("httpie.models.HTTPRequest")
    def test_ovh_auth(self, request, sign, time):
        """Test that headers are filled with expected values by OvhAuth
        implementation."""
        client_id = sentinel.client_id
        client_secret = sentinel.client_secret
        consumer_key = sentinel.consumer_key
        o = httpie_ovh_auth.OvhAuth(client_id, client_secret, consumer_key)
        request.headers = {}
        o(request)
        sign.assert_called_once_with(
            client_secret,
            consumer_key,
            request.method,
            request.url,
            request.body.decode('utf-8'),
            time.return_value,
        )
        assert request.headers["X-Ovh-Application"] == client_id
        assert request.headers["X-Ovh-Consumer"] == consumer_key
        assert request.headers["X-Ovh-Timestamp"] == str(time.return_value)
        assert request.headers["X-Ovh-Signature"] == "$1$" + sign.return_value
