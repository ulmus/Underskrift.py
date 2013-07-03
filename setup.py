#!/usr/bin/env python

from distutils.core import setup

setup(name='Underskrift.py',
      version='0.1.0',
      description='API-wrapper for Underskrift.se',
      long_description=open('README.md').read(),
      author='Jens Alm',
      author_email='jens.alm@prorenata.se',
      url='https://github.com/ulmus/Underskrift.py',
      packages=['underskrift'],
      install_requires=['requests>=1.2.3'],
      license="MIT"
     )