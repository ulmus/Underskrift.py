#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='underskrift',
      version='0.1.0',
      description='API-wrapper for Underskrift.se',
      long_description=open('README.md').read(),
      author='Jens Alm',
      author_email='jens.alm@prorenata.se',
      url='https://github.com/ulmus/Underskrift.py',
      packages=find_packages(),
      install_requires=['requests>=1.2.3'],
      license="MIT"
     )