#!/usr/bin/env python3

from setuptools import setup

setup(name='fetcherd',
      version='0.1',
      description='Python implementation of fetcherd daemon',
      author='David Barnett',
      packages=['fetcherd'],
      package_dir={'fetcherd': 'src/fetcherd'},
      install_requires=[
          'requests',
          'docopts',
          'apscheduler',
          'daemonize',
      ],
      entry_points={
          'console_scripts': [
              'fetcherd=fetchderd.main:main'
          ]
      }
      )
