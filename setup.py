#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import io
from setuptools import setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('httpie_ovh_auth.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

with io.open('requirements.txt', 'rt', encoding='utf-8') as f:
    requirements = f.read()

setup(
    name='httpie-ovh-auth',
    description='OVH auth plugin for HTTPie.',
    version=version,
    author='Laurent Almeras',
    author_email='lalmeras@gmail.com',
    license='BSD',
    url='toto',
    download_url='todo',
    py_modules=['httpie_ovh_auth'],
    zip_safe=False,
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_ovh_auth = httpie_ovh_auth:OvhAuthPlugin'
        ]
    },
    install_requires=requirements.splitlines(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)

