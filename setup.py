#!/usr/bin/env python
# encoding: utf-8

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pytest-ringo',
    license='MIT',
    description='pytest plugin to test webapplications using the Ringo webframework',
    long_description=read("README.md"),
    version='0.2.2',
    author='Torsten Irländer',
    author_email='torsten.irlaender@googlemail.com',
    url='http://github.com/toirl/pytest-ringo/',
    py_modules=['pytest_ringo'],
    entry_points={'pytest11': ['ringo = pytest_ringo']},
    install_requires=['ringo', 'webtest', 'mock', 'coverage', 'pytest-sqlalchemy', 'pytest>=2.0', 'pytest-cov'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ]
)
