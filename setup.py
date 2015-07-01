#!/usr/bin/env python3

from setuptools import setup

setup(name='fetcherd',
      version='0.1',
      description='Python implementation of fetcherd daemon',
      author='David Barnett',
      packages=['fetcherd'],
      package_dir={'fetcherd': 'src/fetcherd'},
      entry_points={
          'console_scripts': [
              'fetcherd = fetcherd.main:main'
          ]
      }
      )
