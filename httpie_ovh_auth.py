# -*- coding: utf-8 -*-
"""
Ovh auth plugin for HTTPie.

"""
import hashlib
import os
import time
from typing import Optional

from httpie.plugins import AuthPlugin
from httpie.models import HTTPRequest

__version__ = "1.2.0"
__author__ = "Laurent Almeras"
__licence__ = "BSD"


def sign(
    secret_key: str,
    consumer_key: str,
    method: str,
    url: str,
    body: str,
    timestamp: float,
) -> str:
    # pylint: disable=too-many-arguments
    """Build and return request signature.

    Signature is hexadecimal representation of SHA1 of the string concatenation
    of :
    secret_key / consumer_key / uppercased HTTP method / url / body / time.

    Integer epoch format is used for time.

    See https://github.com/ovh/python-ovh/blob/master/ovh/client.py
    Client#raw_call method."""
    content = "+".join(
        [
            secret_key,
            consumer_key,
            method.upper(),
            url,
            body if body is not None else "",
            str(int(timestamp)),
        ]
    ).encode("utf-8")
    signature = hashlib.sha1()
    signature.update(content)
    return signature.hexdigest()


class OvhAuth:
    # pylint: disable=too-few-public-methods
    """HTTPie callback implementation to manage OVH authentication.

    See https://github.com/ovh/python-ovh#1-create-an-application

    Attributes:
        client_id           OVH credentials, this variable identifies
                            your application.
        client_secret       OVH credential.
        consumer_key        OVH credential, this is the secret token
                            that links an application with a user
                            account. This consumer secret must be
                            created with a correct scope (method and urls).
    """

    def __init__(self, client_id: str, client_secret: str, consumer_key: str):
        # pylint: disable=unused-argument
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.consumer_key: str = consumer_key

    def __call__(self, request: HTTPRequest) -> HTTPRequest:
        """Authentication implementation.

        ``request`` and credentials are used to build authentication
        related headers:

        * X-Ovh-Application: application key
        * X-Ovh-Consumer: account token for the application
        * X-Ovh-Timestamp and X-Ovh-Signature: signature information
          to prevent any request replay or tampering"""
        now = time.time()
        signature = sign(
            self.client_secret,
            self.consumer_key,
            request.method,
            request.url,
            # request.body is bytes[]; we need str
            request.body.decode('utf-8') if request.body else None,
            now,
        )
        request.headers["X-Ovh-Application"] = self.client_id
        request.headers["X-Ovh-Consumer"] = self.consumer_key
        request.headers["X-Ovh-Timestamp"] = str(int(now))
        request.headers["X-Ovh-Signature"] = "$1$" + signature
        return request


class OvhAuthPlugin(AuthPlugin):
    # pylint: disable=too-few-public-methods
    """OVH Auth plugin for httpie.

    This plugin does not use command line provided authentication parameters.
    It uses environment variable provided credentials.
    """
    name: str = "OVH auth"
    auth_type: str = "ovh"
    description: str = "Authenticate and sign OVH requests"
    auth_require: bool = False
    auth_parse: bool = False
    prompt_password: bool = False

    def __init__(self):
        # httpie arguments not used
        self.client_id: Optional[str] = os.getenv("OVH_CLIENT_ID", None)
        self.client_secret: Optional[str] = os.getenv("OVH_CLIENT_SECRET", None)
        self.consumer_key: Optional[str] = os.getenv("OVH_CONSUMER_KEY", None)

    def get_auth(
        self, username: Optional[str] = None, password: Optional[str] = None
    ) -> OvhAuth:
        if self.client_id and self.client_secret and self.consumer_key:
            return OvhAuth(self.client_id, self.client_secret, self.consumer_key)
        raise OvhAuthException(
            """Credentials not found, check environment
        variables OVH_CLIENT_ID, OVH_CLIENT_SECRET and OVH_CUSTOMER_KEY"""
        )


class OvhAuthException(Exception):
    """OvhAuth exception, raised if plugin cannot be configured or executed."""
