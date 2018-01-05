#! /usr/bin/env python

from setuptools import setup

setup(name = 'ioam-doit',
      description = 'common ioam doit tasks',
      version = '0.1.0',
      license = 'MIT',
      url = 'http://github.com/ioam/ioam-doit',
      py_modules=['ioam_doit'],
      entry_points = {
          'doit.COMMAND': [
              'plug_sample = doit_sample_cmd:SampleCmd'
          ]
      },
      )
