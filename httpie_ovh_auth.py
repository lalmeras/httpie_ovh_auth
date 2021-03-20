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

__version__ = '0.1.0'
__author__ = 'Laurent Almeras'
__licence__ = 'BSD'


def sign(secret_key: str, consumer_key: str,
         method: str, url: str, body: str, timestamp: float) -> str:
    """Build and return request signature."""
    content = "+".join([
            secret_key,
            consumer_key,
            method.upper(),
            url,
            body if body is not None else '',
            str(int(timestamp))
            ]).encode('utf-8')
    signature = hashlib.sha1()
    signature.update(content)
    return signature.hexdigest()


class OvhAuth(object):
    """HTTPie callback implementation to manage OVH authentication.
    
    See https://github.com/ovh/python-ovh#1-create-an-application"""

    """OVH credential - application key. This variable identifies
    your application.
    """
    application_key: str
    """OVH credential - application secret.
    """
    secret_key: str
    """OVH credential - consumer secret. This is the secret token
    that links an application with a user account. This consumer
    secret must be created with a correct scope (method and urls).
    """
    consumer_key: str

    def __init__(self, application_key:str=None, secret_key:str=None,
                 consumer_key:str=None):
        # httpie arguments not used
        self.application_key = os.getenv('OVH_CLIENT_ID', '')
        self.secret_key = os.getenv('OVH_CLIENT_SECRET', '')
        self.consumer_key = os.getenv('OVH_CONSUMER_KEY', '')

    def __call__(self, request:HTTPRequest) -> HTTPRequest:
        """Authentication implementation.

        ``request`` and credentials are used to build authentication
        related headers:
        
        * X-Ovh-Application: application key
        * X-Ovh-Consumer: account token for the application
        * X-Ovh-Timestamp and X-Ovh-Signature: signature information
          to prevent any request replay or tampering"""
        now = time.time()
        signature = sign(self.secret_key, self.consumer_key, request.method,
                         request.url, request.body, now)
        request.headers['X-Ovh-Application'] = self.application_key
        request.headers['X-Ovh-Consumer'] = self.consumer_key
        request.headers['X-Ovh-Timestamp'] = str(int(now))
        request.headers['X-Ovh-Signature'] = "$1$" + signature
        return request


class OvhAuthPlugin(AuthPlugin):
    name:str = 'OVH auth'
    auth_type:str = 'ovh'
    description:str = 'Authenticate and sign OVH requests'
    auth_require:str = False
    auth_parse:str = False
    prompt_password:str = False

    def get_auth(self, username:Optional[str]=None,
                       password:Optional[str]=None) -> OvhAuth:
        # httpie arguments not used
        application_key:str = None
        secret_key:str = None
        consumer_key:str = None

        return OvhAuth(application_key=application_key, secret_key=secret_key,
                consumer_key=consumer_key)

