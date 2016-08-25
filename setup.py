#!/usr/bin/env python3

from distutils.core import setup

setup(name='EDGAR',
      version='0.1',
      description='EDGAR Collection Module',
      long_description='A collection of tools for gathering and interpreting '
                       'financial filings from the SEC EDGAR database.',
      author='Ryan Giarusso',
      author_email='ryangiarusso@gmail.com',
      url='https://github.com/gioGats/EDGAR',
      download_url='https://github.com/gioGats/EDGAR/archive/master.zip',
      packages=['crawling', 'objects', 'objects.ref'],
      platforms=['UNIX'],
      license='Apache License Version 2.0'
      )
