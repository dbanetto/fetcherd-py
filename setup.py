#!/usr/bin/env python3

from setuptools import setup

setup(name='fetcherd',
      version='0.2.0',
      description='Python implementation of fetcherd daemon',
      author='David Barnett',
      packages=['fetcherd', 'fetcherd.sources', 'fetcherd.providers'],
      package_dir={'fetcherd': 'src',
                   'fetcherd.sources': 'src/sources',
                   'fetcherd.providers': 'src/providers',
      },
      data_files=[('config', ['config/config.json'])],
      install_requires=[
          'requests',
          'docopts',
          'bottle',
          'paste'
      ],
      entry_points={
          'console_scripts': [
              'fetcherd=fetcherd.main:main'
          ]
      }
)
