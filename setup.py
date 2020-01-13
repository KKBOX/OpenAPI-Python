#!/usr/bin/env python

"""
Installer for KKBOX SDK
"""

from distutils.core import setup

setup(name='kkbox_developer_sdk',
      description='KKBOX Open API Developer SDK for Python',
      author='KKBOX',
      author_email='willyliu@kkbox.com',
      version='1.0.8',
      url='https://github.com/KKBOX/OpenAPI-Python',
      download_url='https://github.com/KKBOX/OpenAPI-Python/tarball/v1.0.8',
      packages=['kkbox_developer_sdk'],
      package_dir={'kkbox_developer_sdk': 'kkbox_developer_sdk'},
      keywords=['KKBOX', 'Open', 'API', 'OpenAPI'])
