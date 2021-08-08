#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup, Command
import setuptools

NAME = 'apisim'
DESCRIPTION = 'A package to simulate api users.'
URL = 'https://github.com/remcoeijsackers/APIsim'
EMAIL = 'contact@remcoeijsackers.com'
AUTHOR = 'Remco L. Eijsackers'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'


REQUIRED = [
    'certifi', 'cffi', 'chardet', 'cryptography', 'numpy', 'pandas', 'pycparser', 'Pygments', 'python-dateutil', 'PyYAML', 'requests', 'rich', 'six', 'tabulate', 'torpy', 'typing-extensions', 'urllib3'
]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src", exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

    entry_points={
         'console_scripts': ['apisim=src/apisim.py'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)