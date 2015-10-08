#!/usr/bin/env python

import os

from setuptools import setup, find_packages


with open(os.path.join(os.getcwd(), 'requirements.txt')) as f:
    requires = f.read()

setup(
    name='pyramid-node-render-client',
    version='0.0.1',
    description='A node HTML rendering service with React for the Pyramid web framework',
    author='Daniel Gabriele',
    author_email='d.gabri3le@gmail.com',
    packages=find_packages(),
    install_requires=requires,
    tests_require=requires,
)
