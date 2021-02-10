# -*- coding: utf-8 -*-
"""
Ovh auth plugin for HTTPie.

"""
import hashlib
import os
import time

from httpie.plugins import AuthPlugin

__version__ = '0.1.0'
__author__ = 'Laurent Almeras'
__licence__ = 'BSD'


def sign(secret_key: str, consumer_key: str, method: str, url: str, body: str,
         timestamp: float) -> str:
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
    def __init__(self, application_key=None, secret_key=None, consumer_key=None):
        self.application_key = os.getenv('OVH_CLIENT_ID')
        self.secret_key = os.getenv('OVH_CLIENT_SECRET')
        self.consumer_key = os.getenv('OVH_CONSUMER_KEY')

    def __call__(self, request):
        now = time.time()
        signature = sign(self.secret_key, self.consumer_key, request.method,
                         request.url, request.body, now)
        request.headers['X-Ovh-Application'] = self.application_key
        request.headers['X-Ovh-Consumer'] = self.consumer_key
        request.headers['X-Ovh-Timestamp'] = str(int(now))
        request.headers['X-Ovh-Signature'] = "$1$" + signature
        return request


class OvhAuthPlugin(AuthPlugin):
    name = 'OVH auth'
    auth_type = 'ovh'
    description = 'Authenticate and sign OVH requests'
    auth_require = False
    auth_parse = False
    prompt_password = False

    def get_auth(self, username=None, password=None):
        application_key = None
        secret_key = None
        consumer_key = None

        return OvhAuth(application_key=application_key, secret_key=secret_key,
                consumer_key=consumer_key)

