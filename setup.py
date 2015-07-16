#!/usr/bin/env python3

from setuptools import setup

setup(name='fetcherd',
      version='0.1',
      description='Python implementation of fetcherd daemon',
      author='David Barnett',
      packages=['fetcherd', 'fetcherd.sources', 'fetcherd.providers'],
      package_dir={'fetcherd': 'src/fetcherd',
                   'fetcherd.sources': 'src/fetcherd/sources',
                   'fetcherd.providers': 'src/fetcherd/providers'},
      install_requires=[
          'requests',
          'docopts',
          'apscheduler',
          'daemonize',
      ],
      entry_points={
          'console_scripts': [
              'fetcherd=fetcherd.main:main'
          ]
      }
      )
