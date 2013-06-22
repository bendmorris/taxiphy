#!/usr/bin/env python
from distutils.core import setup

setup(name='taxiphy',
      version='0.1',
      description='Generate trees from taxonomies',
      author='Ben Morris',
      author_email='ben@bendmorris.com',
      url='https://github.com/bendmorris/taxiphy',
      packages=['taxiphy'],
      package_dir={
                'taxiphy':''
                },
      entry_points={
        'console_scripts': [
            'taxiphy = taxiphy.taxiphy:main',
        ],
      },
      )