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


class OvhAuth(object):
    def __init__(self, application_key=None, secret_key=None, consumer_key=None):
        self.application_key = os.getenv('OVH_CLIENT_ID')
        self.secret_key = os.getenv('OVH_CLIENT_SECRET')
        self.consumer_key = os.getenv('OVH_CONSUMER_KEY')

    def __call__(self, r):
        now = str(int(time.time()))
        import ipdb
        ipdb.set_trace()
        signature = hashlib.sha1()
        content = "+".join([
            self.secret_key,
            self.consumer_key,
            r.method.upper(),
            r.url,
            r.body if r.body is not None else '',
            now
            ]).encode('utf-8')
        print(content)
        signature.update(content)
        r.headers['X-Ovh-Application'] = self.application_key
        r.headers['X-Ovh-Consumer'] = self.consumer_key
        r.headers['X-Ovh-Timestamp'] = now
        r.headers['X-Ovh-Signature'] = "$1$" + signature.hexdigest()
        return r


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

