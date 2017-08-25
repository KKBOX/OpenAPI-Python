#!/usr/bin/env python

"""
Installer for KKBOX SDK
"""

from distutils.core import setup

setup(name='kkbox_sdk',
      description='KKBOX Open API SDK for Python',
      author='Sharon Yang',
      author_email='sharonyang@kkbox.com',
      version='1.1',
      url='https://github.com/KKBOX/kkbox_openapi_developer_sdk.git',
      packages=['kkbox_sdk'],
      package_dir={'kkbox_sdk': 'kkbox_sdk'})
