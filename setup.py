# -*- coding: utf-8 -*-
#
# This file is part of twikiget.
# Copyright (C) 2019 CERN.
#
# twikiget is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""twikiget."""

import os
import re

from setuptools import setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'isort==4.3.4',
    'coverage>=4.0',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.4.4,<2.0',
        'sphinx-rtd-theme>=0.1.9',
        'sphinx-click>=1.0.4',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for key, reqs in extras_require.items():
    if ':' == key[0]:
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'beautifulsoup4>=4.7.1',
    'click>=7,<8',
    'prettytable>=0.7.2',
    'tablib>=0.12.1',
    'warcio>=1.7.0',
]

# Get the version string. Cannot be done with import!
with open(os.path.join('twikiget', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

setup(
    name='twikiget',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    author='CERN Analysis Preservation',
    author_email='analysis-preservation-team@cern.ch',
    packages=['twikiget', ],
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'twikiget = twikiget.cli:twikiget'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving'
    ]
)
